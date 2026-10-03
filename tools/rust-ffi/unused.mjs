// Present in the dependency closure, but not called by Test.Main. Fail explicitly
// if a new test needs one of these unported APIs; never return a placeholder value.
export const unusedFfi = {
  'Control.Extend': `pub fn Control_Extend_arrayExtend(_f: purust_core::Func1<UnknownType, UnknownType>, _xs: UnknownType) -> UnknownType {
    panic!("Rust FFI not ported for this test runner: Control.Extend.arrayExtend")
}
`,
  'Data.Int.Bits': ['and', 'or', 'xor', 'shl', 'shr', 'zshr', 'complement'].map(name =>
    `pub fn Data_Int_Bits_${name}(_a: i64${name === 'complement' ? '' : ', _b: i64'}) -> i64 {
    panic!("Rust FFI not ported for this test runner: Data.Int.Bits.${name}")
}`).join('\n') + '\n',
  'Performance.Minibench': `pub fn Performance_Minibench_gc() -> UnknownType {
    panic!("Rust FFI not ported for this test runner: Performance.Minibench.gc")
}
pub fn Performance_Minibench_timeNs() -> UnknownType {
    panic!("Rust FFI not ported for this test runner: Performance.Minibench.timeNs")
}
pub fn Performance_Minibench_toFixed(_value: f64) -> String {
    panic!("Rust FFI not ported for this test runner: Performance.Minibench.toFixed")
}
`,
};
