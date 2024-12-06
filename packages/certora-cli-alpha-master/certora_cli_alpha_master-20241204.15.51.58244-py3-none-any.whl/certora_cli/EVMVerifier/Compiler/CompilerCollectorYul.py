import json
from typing import List

from Crypto.Hash import keccak

from EVMVerifier.Compiler.CompilerCollector import CompilerLang
from EVMVerifier.Compiler.CompilerCollectorSol import CompilerLangSol
from EVMVerifier.Compiler.CompilerCollectorSolBased import CompilerCollectorSolBased
from EVMVerifier.certoraContractFuncs import Func
from Shared.certoraUtils import Singleton, CompilerVersion
import EVMVerifier.certoraType as CT


class CompilerLangYul(CompilerLangSol, metaclass=Singleton):
    """
    [CompilerLang] for Yul
    """

    @property
    def name(self) -> str:
        return "Yul"

    @property
    def supports_typed_immutables(self) -> bool:
        return False

    @property
    def supports_ast_output(self) -> bool:
        return False

    @property
    def supports_srclist_output(self) -> bool:
        return False

    @staticmethod
    def get_sighash(name: str, full_args: List[CT.TypeInstance]) -> str:
        sig = Func.compute_signature(name, full_args, lambda x: x.get_source_str())
        f_hash = keccak.new(digest_bits=256)
        f_hash.update(str.encode(sig))

        return f_hash.hexdigest()[0:8]

    def get_funcs(self, yul_abi_json_filepath: str, contract_name: str) -> List[Func]:
        funcs = []
        with open(yul_abi_json_filepath, 'r') as yul_abi_json_file:
            yul_abi_json = json.load(yul_abi_json_file)
            for entry in yul_abi_json:
                if "type" in entry and entry["type"] == "function":
                    name = entry["name"]
                    state_mutability = entry["stateMutability"]
                    full_args = []
                    param_names = []
                    for input in entry["inputs"]:
                        type_name = input["type"]
                        # yul abi is annoying. no better way
                        if type_name.endswith("[]"):
                            base = type_name[:-2]
                            base_type = CT.Type.from_primitive_name(base)
                            out_type: CT.Type = CT.ArrayType(type_name, base_type, None, contract_name, 0)
                        elif type_name == "bytes" or type_name == "string":
                            out_type = CT.PackedBytes()
                        else:
                            out_type = CT.Type.from_primitive_name(type_name)
                        full_args.append(CT.TypeInstance(out_type))
                        param_names.append(input["name"])
                    returns = []
                    for output in entry["outputs"]:
                        type_name = output["type"]
                        # yul abi is annoying. no better way
                        if type_name.endswith("[]"):
                            base = type_name[:-2]
                            base_type = CT.Type.from_primitive_name(base)
                            out_type = CT.ArrayType(type_name, base_type, None, contract_name, 0)
                        elif type_name == "bytes" or type_name == "string":
                            out_type = CT.PackedBytes()
                        else:
                            out_type = CT.Type.from_primitive_name(type_name)
                        returns.append(CT.TypeInstance(out_type))
                    visibility = "external"
                    sighash = self.get_sighash(name, full_args)
                    notpayable = state_mutability in ["nonpayable", "view", "pure"]

                    func = Func(
                        name=name,
                        fullArgs=full_args,
                        paramNames=param_names,
                        returns=returns,
                        sighash=sighash,
                        notpayable=notpayable,
                        fromLib=False,
                        isConstructor=False,
                        stateMutability=state_mutability,
                        visibility=visibility,
                        implemented=True,
                        overrides=False,
                        contractName=contract_name,
                        source_bytes=None,
                        ast_id=None,
                        original_file=None,
                        body_location=None,
                    )
                    funcs.append(func)
        return funcs


class CompilerCollectorYul(CompilerCollectorSolBased):
    def __init__(self, version: CompilerVersion, lang: CompilerLang):
        super().__init__(version, lang)
