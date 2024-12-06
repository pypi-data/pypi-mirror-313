from EVMVerifier.Compiler.CompilerCollector import CompilerCollector, CompilerLang
from Shared.certoraUtils import CompilerVersion


class CompilerCollectorSolBased(CompilerCollector):

    def __init__(self, version: CompilerVersion, lang: CompilerLang):
        self.__compiler_version = version
        self.__smart_contract_lang = lang

    @property
    def compiler_name(self) -> str:
        return self.smart_contract_lang.compiler_name

    @property
    def smart_contract_lang(self) -> CompilerLang:
        return self.__smart_contract_lang

    @property
    def compiler_version(self) -> CompilerVersion:
        return self.__compiler_version
