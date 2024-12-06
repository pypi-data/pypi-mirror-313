error id: OL76yciESTODoiR3+z8qfg==
### Bloop error:

[error response][evaluate]: Cannot evaluate because of failed compilation:
Error while emitting AwkwardCompiler.scala
assertion failed: 
  Cannot create ClassBType from NoSymbol
     while compiling: /tmp/scala-debug-adapter-29141b37d51848749714fb4b2f80ca6818155281624268083065/AwkwardCompiler.scala
        during phase: jvm
     library version: version 2.12.17
    compiler version: version 2.12.12
  reconstructed args: -classpath <WORKSPACE>/.bloop/compilerJVM/bloop-bsp-clients-classes/classes-Metals-HwlBqCPxQqyZYI-oZGrdvA==:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.12.12/scala-library-2.12.12.jar:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/com/github/scopt/scopt_2.12/3.6.0/scopt_2.12-3.6.0.jar:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/com/lihaoyi/fastparse_2.12/1.0.0/fastparse_2.12-1.0.0.jar:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/yaml/snakeyaml/1.28/snakeyaml-1.28.jar:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/com/lihaoyi/fastparse-utils_2.12/1.0.0/fastparse-utils_2.12-1.0.0.jar:<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/com/lihaoyi/sourcecode_2.12/0.1.4/sourcecode_2.12-0.1.4.jar:<HOME>/.cache/bloop/semanticdb/com.sourcegraph.semanticdb-javac.0.9.9/semanticdb-javac-0.9.9.jar -d /tmp/scala-debug-adapter-29141b37d51848749714fb4b2f80ca6818155281624268083065 -Xplugin:<HOME>/.cache/bloop/semanticdb/org.scalameta.semanticdb-scalac_2.12.12.4.8.4/semanticdb-scalac_2.12.12-4.8.4.jar -Xplugin-require:semanticdb -Xsource:3.0.0 -Yrangepos -P:semanticdb:sourceroot:<WORKSPACE> -P:semanticdb:failures:warning -P:semanticdb:synthetics:on

  last tree to typer: Select(Select(Select(Select(Apply(method $asInstanceOf), kaitai), struct), datatype), DataType$EnumType)
       tree position: line 830 of /tmp/scala-debug-adapter-29141b37d51848749714fb4b2f80ca6818155281624268083065/AwkwardCompiler.scala
            tree tpe: io.kaitai.struct.datatype.DataType$EnumType.type
              symbol: object DataType$EnumType in package datatype
   symbol definition: object DataType$EnumType (a ModuleSymbol)
      symbol package: io.kaitai.struct.datatype
       symbol owners: object DataType$EnumType
           call site: method $anonfun$createBuilderStructure$2$adapted in object Expression29141b37d51848749714fb4b2f80ca68 in package languages

== Source file context for tree position ==

   827           var builderName = idToStr(id)
   828           outSrc.puts(s"auto& ${builderName}_indexbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>();")
   829           outSrc.puts(s"auto& ${builderName}_stringbuilder = ${builderName}_indexbuilder.append_index();")
   830           outSrc.puts(s"""${builderName}_indexbuilder.set_parameters("\\"__array__\\": \\"categorical\\"");""")
   831           // enumType.enumSpec.value.map.elems0.foreach { case (_, enumValue) =>
   832           //   if (enumValue.key == getRawIdExpr(id, rep)) {
   833           //   outSrc.puts(s"""${builderName}_stringbuilder.append("${enumValue.value.name}");""").
#### Short summary: 

[error response][evaluate]: Cannot evaluate because of failed compilation:
Error while emitting Awkw...