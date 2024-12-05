from logging import getLogger

from dls_pmacanalyse.pmacparser import PmacParser
from dls_pmacanalyse.pmacvariables import PmacToken, PmacVariable
from dls_pmacanalyse.utils import (
    compareFloats,
    isNumber,
    isString,
    stripStringQuotes,
    tokenToInt,
    toNumber,
)

log = getLogger(__name__)


class PmacProgram(PmacVariable):
    def __init__(self, prefix, n, v, lines=None, offsets=None):
        PmacVariable.__init__(self, prefix, n, v)
        self.offsets = offsets
        self.lines: list[str] = lines or []

    def add(self, t):
        if not isinstance(t, PmacToken):
            log.warning(f"PmacProgram: {repr(t)} is not a token")
        self.v.append(t)

    def clear(self):
        self.v = []

    def valueText(self, typ=0, ignore_ret=False):
        result = ""
        last_line = len(self.v) - 1
        for i, t in enumerate(self.v):
            if t == "\n":
                if len(result) > 0 and not result[-1] == "\n":
                    result += str(t)
            elif not ignore_ret or t != "RETURN" or i < last_line:
                if len(result) == 0:
                    pass
                elif result[-1].isalpha() and str(t)[0].isalpha():
                    result += " "
                elif result[-1].isdigit() and str(t)[0].isdigit():
                    result += " "
                result += str(t)
                if typ == 1 and len(result.rsplit("\n", 1)[-1]) > 60:
                    result += "\n"
        if len(result) == 0 or result[-1] != "\n":
            result += "\n"
        return result

    def compare(self, other):
        # Strip the newline tokens from the two lists.  There's
        # probably a better way of doing this.
        a = []
        for i in self.v:
            if i == "\n":
                pass
            else:
                a.append(i)
        b = []
        for i in other.v:
            if i == "\n":
                pass
            else:
                b.append(i)
        # Now compare them token by token
        result = True
        while len(a) > 0 and len(b) > 0:
            # Extract the current head token from each list
            a0 = a[0]
            b0 = b[0]
            a[0:1] = []
            b[0:1] = []
            # Compare them
            if isNumber(a0) and isNumber(b0):
                if not compareFloats(toNumber(a0), toNumber(b0), 0.00001):
                    result = False
                    a0.compareFail = True
                    b0.compareFail = True
            elif a0 == "COMMAND" and b0 == "COMMAND" and len(a) > 0 and len(b) > 0:
                # Get the command strings
                a0 = a[0]
                b0 = b[0]
                a[0:1] = []
                b[0:1] = []
                if isString(str(a0)) and isString(str(b0)):
                    # Parse them
                    parserA = PmacParser([stripStringQuotes(str(a0))], self)
                    varA = PmacCommandString(parserA.tokens())
                    parserB = PmacParser([stripStringQuotes(str(b0))], self)
                    varB = PmacCommandString(parserB.tokens())
                    if not varA.compare(varB):
                        result = False
                        a0.compareFail = True
                        b0.compareFail = True
                else:
                    if a0 != b0:
                        result = False
                        a0.compareFail = True
                        b0.compareFail = True
            else:
                if a0 != b0:
                    result = False
                    a0.compareFail = True
                    b0.compareFail = True
        for a0 in a:
            a0.compareFail = True
            result = False
        for b0 in b:
            b0.compareFail = True
            result = False
        return result

    def html(self, page, parent):
        lines = self.valueText(typ=1).split()
        for line in lines:
            page.text(parent, line)
            page.lineBreak(parent)

    def html2(self, page, parent):
        text = ""
        for i in range(len(self.lines)):
            text += f"{self.offsets[i]}:\t{self.lines[i]}\n"
        page.paragraph(parent, text, id="code")

    def isEmpty(self):
        a = []
        for i in self.v:
            if i == "\n":
                pass
            else:
                a.append(i)
        return len(a) == 0 or a == ["RETURN"]

    def htmlCompare(self, page, parent, other):
        lineLen = 0
        for t in self.v:
            if t == "\n":
                if lineLen > 0:
                    page.lineBreak(parent)
                    lineLen = 0
            else:
                if t.compareFail:
                    page.text(page.emphasize(parent), t)
                else:
                    page.text(parent, t)
                lineLen += len(t)
                if lineLen > 60:
                    page.lineBreak(parent)
                    lineLen = 0


class PmacPlcProgram(PmacProgram):
    def __init__(self, n, v=None, lines=None, offsets=None):
        if v is None:
            v = []
        PmacProgram.__init__(self, "plc", n, v, lines, offsets)
        self.isRunning = False
        self.shouldBeRunning = False

    def dump(self, typ=0):
        if typ == 1:
            result = self.valueText()
        else:
            result = ""
            if len(self.v) > 0:
                result = f"\nopen plc {self.n} clear\n"
                result += self.valueText(ignore_ret=True)
                result += "close\n"
        return result

    def copyFrom(self):
        result = PmacPlcProgram(self.n)
        result.v = self.v
        result.ro = self.ro
        result.offsets = self.offsets
        result.lines = self.lines
        return result

    def setShouldBeRunning(self):
        """
        Sets the shouldBeRunning flag if the PLC does not contain a disable
        statement for itself.
        """
        self.shouldBeRunning = True
        state = "idle"
        for i in self.v:
            if state == "idle":
                if i == "DISABLE":
                    state = "disable"
            elif state == "disable":
                if i == "PLC":
                    state = "plc"
                else:
                    state = "idle"
            elif state == "plc":
                if tokenToInt(i) == self.n:
                    self.shouldBeRunning = False
                state = "idle"

    def setIsRunning(self, state):
        self.isRunning = state


class PmacCommandString(PmacProgram):
    def __init__(self, v):
        PmacProgram.__init__(self, "CMD", 0, v)


class PmacCsAxisDef(PmacProgram):
    def __init__(self, cs, n, v=None):
        if v is None:
            v = [PmacToken("0")]
        PmacProgram.__init__(self, f"&{cs}#", n, v)
        self.cs = cs

    def dump(self, typ=0):
        if typ == 1:
            result = f"{self.valueText()}"
        else:
            result = f"&{self.cs}#{self.n}->{self.valueText()}"
        return result

    def isZero(self):
        result = True
        for t in self.v:
            if t == "0" or t == "0.0" or t == "\n":
                pass
            else:
                result = False
        return result

    def copyFrom(self):
        result = PmacCsAxisDef(self.cs, self.n)
        result.v = self.v
        result.ro = self.ro
        result.offsets = self.offsets
        result.lines = self.lines
        return result


class PmacForwardKinematicProgram(PmacProgram):
    def __init__(self, n, v=None):
        if v is None:
            v = []
        PmacProgram.__init__(self, "fwd", n, v)

    def dump(self, typ=0):
        if typ == 1:
            result = self.valueText()
        else:
            result = ""
            if len(self.v) > 0:
                result = f"\n&{self.n} open forward clear\n"
                result += self.valueText(ignore_ret=True)
                result += "close\n"
        return result

    def copyFrom(self):
        result = PmacForwardKinematicProgram(self.n)
        result.v = self.v
        result.ro = self.ro
        result.offsets = self.offsets
        result.lines = self.lines
        return result


class PmacInverseKinematicProgram(PmacProgram):
    def __init__(self, n, v=None):
        if v is None:
            v = []
        PmacProgram.__init__(self, "inv", n, v)

    def dump(self, typ=0):
        if typ == 1:
            result = self.valueText()
        else:
            result = ""
            if len(self.v) > 0:
                result = f"\n&{self.n} open inverse clear\n"
                result += self.valueText(ignore_ret=True)
                result += "close\n"
        return result

    def copyFrom(self):
        result = PmacInverseKinematicProgram(self.n)
        result.v = self.v
        result.ro = self.ro
        result.offsets = self.offsets
        result.lines = self.lines
        return result


class PmacMotionProgram(PmacProgram):
    def __init__(self, n, v=None, lines=None, offsets=None):
        if v is None:
            v = []
        PmacProgram.__init__(self, "prog", n, v, lines, offsets)

    def dump(self, typ=0):
        if typ == 1:
            result = self.valueText()
        else:
            result = ""
            if len(self.v) > 0:
                result = f"\nopen program {self.n} clear\n"
                result += self.valueText(ignore_ret=True)
                result += "close\n"
        return result

    def copyFrom(self):
        result = PmacMotionProgram(self.n)
        result.v = self.v
        result.ro = self.ro
        result.offsets = self.offsets
        result.lines = self.lines
        return result
