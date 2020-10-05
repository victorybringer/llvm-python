; ModuleID = 'divide3.ll'
source_filename = "divide3.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @g(i32) #0 !dbg !7 {
  call void @llvm.dbg.value(metadata i32 %0, metadata !11, metadata !DIExpression()), !dbg !12
  %2 = add nsw i32 %0, 9, !dbg !13
  call void @llvm.dbg.value(metadata i32 %2, metadata !14, metadata !DIExpression()), !dbg !15
  %3 = sub nsw i32 %0, 7, !dbg !16
  %4 = add nsw i32 %3, %2, !dbg !17
  call void @llvm.dbg.value(metadata i32 %4, metadata !18, metadata !DIExpression()), !dbg !19
  %5 = mul nsw i32 2, %4, !dbg !20
  %6 = add nsw i32 %2, %5, !dbg !21
  call void @llvm.dbg.value(metadata i32 %6, metadata !11, metadata !DIExpression()), !dbg !12
  %7 = add nsw i32 %6, 12, !dbg !22
  %8 = sub nsw i32 100, %7, !dbg !23
  call void @llvm.dbg.value(metadata i32 %8, metadata !24, metadata !DIExpression()), !dbg !25
  %9 = icmp sgt i32 %8, -1, !dbg !26
  br i1 %9, label %10, label %12, !dbg !28

; <label>:10:                                     ; preds = %1
  %11 = sdiv i32 100, %8, !dbg !29
  call void @llvm.dbg.value(metadata i32 %11, metadata !31, metadata !DIExpression()), !dbg !32
  br label %12, !dbg !33

; <label>:12:                                     ; preds = %10, %1
  ret i32 undef, !dbg !34
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32) #0 !dbg !35 {
  call void @llvm.dbg.value(metadata i32 %0, metadata !36, metadata !DIExpression()), !dbg !37
  %2 = add nsw i32 %0, 3, !dbg !38
  call void @llvm.dbg.value(metadata i32 %2, metadata !39, metadata !DIExpression()), !dbg !40
  %3 = icmp sgt i32 %2, 5, !dbg !41
  br i1 %3, label %6, label %4, !dbg !43

; <label>:4:                                      ; preds = %1
  %5 = icmp slt i32 %2, 0, !dbg !44
  br i1 %5, label %6, label %8, !dbg !45

; <label>:6:                                      ; preds = %4, %1
  %7 = add nsw i32 %2, 2, !dbg !46
  call void @llvm.dbg.value(metadata i32 %7, metadata !39, metadata !DIExpression()), !dbg !40
  br label %10, !dbg !47

; <label>:8:                                      ; preds = %4
  %9 = sub nsw i32 %2, 5, !dbg !48
  call void @llvm.dbg.value(metadata i32 %9, metadata !39, metadata !DIExpression()), !dbg !40
  br label %10

; <label>:10:                                     ; preds = %8, %6
  %.0 = phi i32 [ %7, %6 ], [ %9, %8 ], !dbg !49
  call void @llvm.dbg.value(metadata i32 %.0, metadata !39, metadata !DIExpression()), !dbg !40
  %11 = call i32 @g(i32 %.0), !dbg !50
  ret i32 0, !dbg !51
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.value(metadata, metadata, metadata) #1

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 8.0.1-9 (tags/RELEASE_801/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, nameTableKind: None)
!1 = !DIFile(filename: "divide3.c", directory: "/libx32/llvmlite")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
!7 = distinct !DISubprogram(name: "g", scope: !1, file: !1, line: 5, type: !8, scopeLine: 5, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!8 = !DISubroutineType(types: !9)
!9 = !{!10, !10}
!10 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!11 = !DILocalVariable(name: "x", arg: 1, scope: !7, file: !1, line: 5, type: !10)
!12 = !DILocation(line: 5, column: 11, scope: !7)
!13 = !DILocation(line: 10, column: 10, scope: !7)
!14 = !DILocalVariable(name: "z", scope: !7, file: !1, line: 10, type: !10)
!15 = !DILocation(line: 10, column: 6, scope: !7)
!16 = !DILocation(line: 12, column: 10, scope: !7)
!17 = !DILocation(line: 12, column: 12, scope: !7)
!18 = !DILocalVariable(name: "t", scope: !7, file: !1, line: 12, type: !10)
!19 = !DILocation(line: 12, column: 6, scope: !7)
!20 = !DILocation(line: 15, column: 9, scope: !7)
!21 = !DILocation(line: 15, column: 7, scope: !7)
!22 = !DILocation(line: 17, column: 16, scope: !7)
!23 = !DILocation(line: 17, column: 13, scope: !7)
!24 = !DILocalVariable(name: "y", scope: !7, file: !1, line: 17, type: !10)
!25 = !DILocation(line: 17, column: 6, scope: !7)
!26 = !DILocation(line: 19, column: 6, scope: !27)
!27 = distinct !DILexicalBlock(scope: !7, file: !1, line: 19, column: 4)
!28 = !DILocation(line: 19, column: 4, scope: !7)
!29 = !DILocation(line: 20, column: 15, scope: !30)
!30 = distinct !DILexicalBlock(scope: !27, file: !1, line: 19, column: 12)
!31 = !DILocalVariable(name: "z", scope: !30, file: !1, line: 20, type: !10)
!32 = !DILocation(line: 20, column: 7, scope: !30)
!33 = !DILocation(line: 21, column: 1, scope: !30)
!34 = !DILocation(line: 23, column: 1, scope: !7)
!35 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 27, type: !8, scopeLine: 27, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!36 = !DILocalVariable(name: "x", arg: 1, scope: !35, file: !1, line: 27, type: !10)
!37 = !DILocation(line: 27, column: 15, scope: !35)
!38 = !DILocation(line: 29, column: 8, scope: !35)
!39 = !DILocalVariable(name: "y", scope: !35, file: !1, line: 29, type: !10)
!40 = !DILocation(line: 29, column: 5, scope: !35)
!41 = !DILocation(line: 31, column: 5, scope: !42)
!42 = distinct !DILexicalBlock(scope: !35, file: !1, line: 31, column: 4)
!43 = !DILocation(line: 31, column: 8, scope: !42)
!44 = !DILocation(line: 31, column: 12, scope: !42)
!45 = !DILocation(line: 31, column: 4, scope: !35)
!46 = !DILocation(line: 33, column: 4, scope: !42)
!47 = !DILocation(line: 33, column: 1, scope: !42)
!48 = !DILocation(line: 37, column: 4, scope: !42)
!49 = !DILocation(line: 0, scope: !42)
!50 = !DILocation(line: 40, column: 1, scope: !35)
!51 = !DILocation(line: 42, column: 1, scope: !35)
