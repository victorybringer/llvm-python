; ModuleID = 'divide3.c'
source_filename = "divide3.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @g(i32) #0 !dbg !7 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !11, metadata !DIExpression()), !dbg !12
  call void @llvm.dbg.declare(metadata i32* %4, metadata !13, metadata !DIExpression()), !dbg !14
  %8 = load i32, i32* %3, align 4, !dbg !15
  %9 = add nsw i32 %8, 9, !dbg !16
  store i32 %9, i32* %4, align 4, !dbg !14
  call void @llvm.dbg.declare(metadata i32* %5, metadata !17, metadata !DIExpression()), !dbg !18
  %10 = load i32, i32* %3, align 4, !dbg !19
  %11 = sub nsw i32 %10, 7, !dbg !20
  %12 = load i32, i32* %4, align 4, !dbg !21
  %13 = add nsw i32 %11, %12, !dbg !22
  store i32 %13, i32* %5, align 4, !dbg !18
  %14 = load i32, i32* %4, align 4, !dbg !23
  %15 = load i32, i32* %5, align 4, !dbg !24
  %16 = mul nsw i32 2, %15, !dbg !25
  %17 = add nsw i32 %14, %16, !dbg !26
  store i32 %17, i32* %3, align 4, !dbg !27
  call void @llvm.dbg.declare(metadata i32* %6, metadata !28, metadata !DIExpression()), !dbg !29
  %18 = load i32, i32* %3, align 4, !dbg !30
  %19 = add nsw i32 %18, 12, !dbg !31
  %20 = sub nsw i32 100, %19, !dbg !32
  store i32 %20, i32* %6, align 4, !dbg !29
  %21 = load i32, i32* %6, align 4, !dbg !33
  %22 = icmp sgt i32 %21, -1, !dbg !35
  br i1 %22, label %23, label %26, !dbg !36

; <label>:23:                                     ; preds = %1
  call void @llvm.dbg.declare(metadata i32* %7, metadata !37, metadata !DIExpression()), !dbg !39
  %24 = load i32, i32* %6, align 4, !dbg !40
  %25 = sdiv i32 100, %24, !dbg !41
  store i32 %25, i32* %7, align 4, !dbg !39
  br label %26, !dbg !42

; <label>:26:                                     ; preds = %23, %1
  %27 = load i32, i32* %2, align 4, !dbg !43
  ret i32 %27, !dbg !43
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32) #0 !dbg !44 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, i32* %2, align 4
  store i32 %0, i32* %3, align 4
  call void @llvm.dbg.declare(metadata i32* %3, metadata !45, metadata !DIExpression()), !dbg !46
  call void @llvm.dbg.declare(metadata i32* %4, metadata !47, metadata !DIExpression()), !dbg !48
  %5 = load i32, i32* %3, align 4, !dbg !49
  %6 = add nsw i32 %5, 3, !dbg !50
  store i32 %6, i32* %4, align 4, !dbg !48
  %7 = load i32, i32* %4, align 4, !dbg !51
  %8 = icmp sgt i32 %7, 5, !dbg !53
  br i1 %8, label %12, label %9, !dbg !54

; <label>:9:                                      ; preds = %1
  %10 = load i32, i32* %4, align 4, !dbg !55
  %11 = icmp slt i32 %10, 0, !dbg !56
  br i1 %11, label %12, label %15, !dbg !57

; <label>:12:                                     ; preds = %9, %1
  %13 = load i32, i32* %4, align 4, !dbg !58
  %14 = add nsw i32 %13, 2, !dbg !59
  store i32 %14, i32* %4, align 4, !dbg !60
  br label %18, !dbg !61

; <label>:15:                                     ; preds = %9
  %16 = load i32, i32* %4, align 4, !dbg !62
  %17 = sub nsw i32 %16, 5, !dbg !63
  store i32 %17, i32* %4, align 4, !dbg !64
  br label %18

; <label>:18:                                     ; preds = %15, %12
  %19 = load i32, i32* %4, align 4, !dbg !65
  %20 = call i32 @g(i32 %19), !dbg !66
  %21 = load i32, i32* %2, align 4, !dbg !67
  ret i32 %21, !dbg !67
}

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
!13 = !DILocalVariable(name: "z", scope: !7, file: !1, line: 10, type: !10)
!14 = !DILocation(line: 10, column: 6, scope: !7)
!15 = !DILocation(line: 10, column: 9, scope: !7)
!16 = !DILocation(line: 10, column: 10, scope: !7)
!17 = !DILocalVariable(name: "t", scope: !7, file: !1, line: 12, type: !10)
!18 = !DILocation(line: 12, column: 6, scope: !7)
!19 = !DILocation(line: 12, column: 9, scope: !7)
!20 = !DILocation(line: 12, column: 10, scope: !7)
!21 = !DILocation(line: 12, column: 13, scope: !7)
!22 = !DILocation(line: 12, column: 12, scope: !7)
!23 = !DILocation(line: 15, column: 6, scope: !7)
!24 = !DILocation(line: 15, column: 10, scope: !7)
!25 = !DILocation(line: 15, column: 9, scope: !7)
!26 = !DILocation(line: 15, column: 7, scope: !7)
!27 = !DILocation(line: 15, column: 4, scope: !7)
!28 = !DILocalVariable(name: "y", scope: !7, file: !1, line: 17, type: !10)
!29 = !DILocation(line: 17, column: 6, scope: !7)
!30 = !DILocation(line: 17, column: 15, scope: !7)
!31 = !DILocation(line: 17, column: 16, scope: !7)
!32 = !DILocation(line: 17, column: 13, scope: !7)
!33 = !DILocation(line: 19, column: 4, scope: !34)
!34 = distinct !DILexicalBlock(scope: !7, file: !1, line: 19, column: 4)
!35 = !DILocation(line: 19, column: 6, scope: !34)
!36 = !DILocation(line: 19, column: 4, scope: !7)
!37 = !DILocalVariable(name: "z", scope: !38, file: !1, line: 20, type: !10)
!38 = distinct !DILexicalBlock(scope: !34, file: !1, line: 19, column: 12)
!39 = !DILocation(line: 20, column: 7, scope: !38)
!40 = !DILocation(line: 20, column: 17, scope: !38)
!41 = !DILocation(line: 20, column: 15, scope: !38)
!42 = !DILocation(line: 21, column: 1, scope: !38)
!43 = !DILocation(line: 23, column: 1, scope: !7)
!44 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 27, type: !8, scopeLine: 27, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!45 = !DILocalVariable(name: "x", arg: 1, scope: !44, file: !1, line: 27, type: !10)
!46 = !DILocation(line: 27, column: 15, scope: !44)
!47 = !DILocalVariable(name: "y", scope: !44, file: !1, line: 29, type: !10)
!48 = !DILocation(line: 29, column: 5, scope: !44)
!49 = !DILocation(line: 29, column: 7, scope: !44)
!50 = !DILocation(line: 29, column: 8, scope: !44)
!51 = !DILocation(line: 31, column: 4, scope: !52)
!52 = distinct !DILexicalBlock(scope: !44, file: !1, line: 31, column: 4)
!53 = !DILocation(line: 31, column: 5, scope: !52)
!54 = !DILocation(line: 31, column: 8, scope: !52)
!55 = !DILocation(line: 31, column: 11, scope: !52)
!56 = !DILocation(line: 31, column: 12, scope: !52)
!57 = !DILocation(line: 31, column: 4, scope: !44)
!58 = !DILocation(line: 33, column: 3, scope: !52)
!59 = !DILocation(line: 33, column: 4, scope: !52)
!60 = !DILocation(line: 33, column: 2, scope: !52)
!61 = !DILocation(line: 33, column: 1, scope: !52)
!62 = !DILocation(line: 37, column: 3, scope: !52)
!63 = !DILocation(line: 37, column: 4, scope: !52)
!64 = !DILocation(line: 37, column: 2, scope: !52)
!65 = !DILocation(line: 40, column: 3, scope: !44)
!66 = !DILocation(line: 40, column: 1, scope: !44)
!67 = !DILocation(line: 42, column: 1, scope: !44)
