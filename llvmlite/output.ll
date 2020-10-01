; ModuleID = 'divide3.ll'
source_filename = "divide3.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @g(i32) #0 {
  %2 = add nsw i32 %0, 9
  %3 = sub nsw i32 %0, 7
  %4 = add nsw i32 %3, %2
  %5 = mul nsw i32 2, %4
  %6 = add nsw i32 %2, %5
  %7 = add nsw i32 %6, 12
  %8 = sdiv i32 100, %7
  ret i32 %8
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32) #0 {
  %2 = icmp slt i32 %0, 0
  br i1 %2, label %3, label %5

; <label>:3:                                      ; preds = %1
  %4 = call i32 @g(i32 %0)
  br label %5

; <label>:5:                                      ; preds = %3, %1
  ret i32 0
}

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
