from ..errorHandling         import ErrorHandlerVariables

class ProgramDefinitions:
    def __init__(self , mem, variables, tags, runner=None):
        self.__mem       = variables.getMemory()
        self.__variables = variables
        self.__tags      = tags
        self.runner      = runner

    def cargar(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def almacene(self, name):  # * works
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            exit()  # ! must send index to the end of the file
            return
        prev = self.__variables.getValue(name)
        new  = self.__mem.getAcumulador()
        self.__variables.setValue(name, new)
        self.__mem.saveStep(name, prev, new)

    def nueva(self, name, type_, value):  # !
        if self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_ya_declarada(name)
            return
        value = self.check_type(type_, value)
        self.__variables.setValue(name, value)
        self.__mem.saveStep(name, value)

    def check_type(self, type_, value):
        try:
            if(type_ == "C"):
                value = str(value)
            if(type_ == "I"):
                value = int(value)
            if(type_ == "R"):
                value = float(value)
            if(type_ == "L"):
                value = int(value)
                value = bool(value)
            return value
        except TypeError:
            ErrorHandlerVariables.throw_operando_no_es_numero()
            exit()

    def vaya(self,tag):
        if not self.__tags.inDeclarations(tag):
            ErrorHandlerVariables.throw_tag_no_declarada(tag)
            return
        self.runner.setLine(self.__tags.getValue(tag) -1)

    def vayasi(self, tag1, tag2):
        if not self.__tags.inDeclarations(tag1):
            ErrorHandlerVariables.throw_tag_no_declarada(tag1)
            exit()
            return
        if not self.__tags.inDeclarations(tag2):
            ErrorHandlerVariables.throw_tag_no_declarada(tag2)
            exit()
            return
        prev = self.runner.getCurrentLine()
        if self.__mem.getAcumulador() > 0:
            self.runner.setLine(self.__tags.getValue(tag1) -1) # makes it equal to the value in tag1
            self.__mem.saveStep("vayasi",str(" desde " + str(prev)+ " hasta "), self.runner.getCurrentLine())
            return
        if self.__mem.getAcumulador() < 0:
            self.runner.setLine(self.__tags.getValue(tag2)-1) # makes it equal to the value in tag2
            self.__mem.saveStep("vayasi", str(" desde " + str(prev)+ " hasta ") , self.runner.getCurrentLine())
            return
        self.__mem.saveStep("vayasi",str("desde " + str(prev)+ " hasta ") , self.runner.getCurrentLine())

    def etiqueta(self, name, value):
        if self.__tags.inDeclarations(name):
            ErrorHandlerVariables.throw_tag_ya_declarada(name)
            return
        try:
            value = int(value)
        except:
            ErrorHandlerVariables.throw_operando_no_es_numero()
            exit()
        self.__tags.setValue(name, value)
        self.__mem.saveStep(name, value)

    def lea(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev  = self.__variables.getValue(name)
        value = int(input("ingrese valor"))

        self.__variables.setValue(name, value)
        self.__mem.saveStep(name, value)


    def sume(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() + self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def reste(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() - self.__variables.getValue(name)
        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def multiplique(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new = self.__mem.getAcumulador() * self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def divida(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        if self.__variables.getValue(name) == 0:
            ErrorHandlerVariables.throw_division_por_cero(
                self.__mem.getAcumulador(), self.__variables.getValue(name))
            return
        
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() / self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def potencia(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() ** self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def modulo(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() % self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def concatene(self, name):  # ! variable value has to be a string
        if not self.__variables.inDeclarations(name):
            # if not a variable then is a normal string to concat
            self.__mem.setAcumulador(str(self.__mem.getAcumulador()) + name)
            return
        prev = self.__mem.getAcumulador()
        new = str(self.__mem.getAcumulador()) + self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStep("Acumulador", prev, new)

    def elimine(self, to_delete):
        if type(self.__mem.getAcumulador()) != str:
            ErrorHandlerVariables.throw_acu_not_string()
            return
        subcadena = self.__mem.getAcumulador().strip(to_delete)

    def extraiga(self, substr):
        subcadena = self.__mem.getAcumulador()[:substr]

    def Y(self, first, second, ans):
        self.__variables.setValue(ans, True if self.__variables.getValue(
            first) and self.__variables.getValue(second) else False)

    def O(self, first, second, ans):
        self.__variables.setValue(ans, True if self.__variables.getValue(
            first) or self.__variables.getValue(second) else False)

    def NO(self, first, ans):
        self.__variables.setValue(ans, not self.__variables.getValue(first))

    def muestre(self, name):
        if(name == "acumulador"):
            print(self.__mem.getAcumulador())
            return
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        value = self.__variables.getValue(name)
        self.runner.appendStdout(value)
        self.__mem.saveStep(name, value)

    def imprima(self):  # !!!!!!!!
        pass

    def max_(self, a, b):
        if(type(a) == str and type(b) == str):
            return self.__variables.getValue(a) if self.__variables.getValue(a) > self.__variables.getValue(b) else self.__variables.getValue(b)
        if(type(a) == str and b == int):
            return self.__variables.getValue(a) if self.__variables.getValue(a) > b else b
        if(a == int and type(b) == str):
            return a if a > self.__variables.getValue(b) else self.__variables.getValue(b)
        return a if a > b else b

    def returne(self, value):
        self.__mem.saveStep("returne", value)
        return
