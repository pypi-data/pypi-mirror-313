/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace arith {
class FastMathFlagsAttr;
class IntegerOverflowFlagsAttr;
class DenormalModeAttr;
namespace detail {
struct FastMathFlagsAttrStorage;
} // namespace detail
class FastMathFlagsAttr : public ::mlir::Attribute::AttrBase<FastMathFlagsAttr, ::mlir::Attribute, detail::FastMathFlagsAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "arith.fastmath";
  static constexpr ::llvm::StringLiteral dialectName = "arith";
  static FastMathFlagsAttr get(::mlir::MLIRContext *context, ::mlir::arith::FastMathFlags value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"fastmath"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::arith::FastMathFlags getValue() const;
};
namespace detail {
struct IntegerOverflowFlagsAttrStorage;
} // namespace detail
class IntegerOverflowFlagsAttr : public ::mlir::Attribute::AttrBase<IntegerOverflowFlagsAttr, ::mlir::Attribute, detail::IntegerOverflowFlagsAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "arith.overflow";
  static constexpr ::llvm::StringLiteral dialectName = "arith";
  static IntegerOverflowFlagsAttr get(::mlir::MLIRContext *context, ::mlir::arith::IntegerOverflowFlags value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"overflow"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::arith::IntegerOverflowFlags getValue() const;
};
namespace detail {
struct DenormalModeAttrStorage;
} // namespace detail
class DenormalModeAttr : public ::mlir::Attribute::AttrBase<DenormalModeAttr, ::mlir::Attribute, detail::DenormalModeAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "arith.denormal";
  static constexpr ::llvm::StringLiteral dialectName = "arith";
  static DenormalModeAttr get(::mlir::MLIRContext *context, ::mlir::arith::DenormalMode value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"denormal"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::arith::DenormalMode getValue() const;
};
} // namespace arith
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::arith::FastMathFlagsAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::arith::IntegerOverflowFlagsAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::arith::DenormalModeAttr)

#endif  // GET_ATTRDEF_CLASSES

