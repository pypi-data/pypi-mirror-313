package io.kaitai.struct.languages

import io.kaitai.struct.CppRuntimeConfig._
import io.kaitai.struct._
import io.kaitai.struct.datatype.DataType._
import io.kaitai.struct.datatype._
import io.kaitai.struct.exprlang.Ast
import io.kaitai.struct.exprlang.Ast.expr
import io.kaitai.struct.format._
import io.kaitai.struct.languages.components._
import io.kaitai.struct.translators.{AwkwardTranslator, TypeDetector}
import scala.collection.immutable.Map
import scala.collection.mutable.{Map => MutableMap, ListBuffer, Set, Stack}


class AwkwardCompiler(
  typeProvider: ClassTypeProvider,
  config: RuntimeConfig
) extends LanguageCompiler(typeProvider, config)
    with ObjectOrientedLanguage
    with AllocateAndStoreIO
    with FixedContentsUsingArrayByteLiteral
    with UniversalDoc
    with SwitchIfOps
    with EveryReadIsExpression {
  import AwkwardCompiler._

  val importListSrc = new CppImportList
  val importListHdr = new CppImportList

  override val translator = new AwkwardTranslator(typeProvider, importListSrc, importListHdr, config)
  val outSrcHeader = new StringLanguageOutputWriter(indent)
  val outHdrHeader = new StringLanguageOutputWriter(indent)
  val outSrc = new StringLanguageOutputWriter(indent)
  val outHdr = new StringLanguageOutputWriter(indent)
  val outHdrAwkward = new StringLanguageOutputWriter(indent)
  val outSrcAwkward = new StringLanguageOutputWriter(indent)
  val uniqueSetRecord: Set[String] = Set()

  override def results(topClass: ClassSpec): Map[String, String] = {
    val className = topClass.nameAsStr
    Map(
      outFileNameSource(className) -> (outSrcHeader.result + importListSrc.result + outSrcAwkward.result + outSrc.result),
      outFileNameHeader(className) -> (outHdrHeader.result + importListHdr.result + outHdrAwkward.result + outHdr.result),
    )
  }

/**
  * Trait for generating the LayoutBuilder structure and builder
  * strings for the given ksy file.
  */
  trait LayoutBuilder {
    /**
      * Prints the structure of the generated LayoutBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return strings containing the type of the builder, its contents and
      * other strings associated with the builder.
      */
    def printBuilderStructure(indent: Int = 0): String
  }

  /**
    * Generates the NumpyBuilder structure.
    * @param dataType the type of data in NumpyBuilder.
    */
  case class NumpyBuilder(
    dataType: String
  ) extends LayoutBuilder {

    /**
      * Prints the structure of NumpyBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return string containing the primitive data type of NumpyBuilder buffer.
      */
    override def printBuilderStructure(indent: Int): String = {
      s"NumpyBuilder<$dataType>"
    }
  }

  /**
    * Generates the StringBuilder structure.
    * @param dataType the type of data in StringBuilder.
    */
  case class StringBuilder(
    dataType: String
  ) extends LayoutBuilder {

    /**
      * Prints the structure of StringBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return string containing the primitive data type of StringBuilder buffer.
      */
    override def printBuilderStructure(indent: Int): String = {
      s"StringBuilder<$dataType>"
    }
  }
  /**
    * Generates the ListOffsetBuilder structure.
    * @param offsets the type of `offsets` buffer.
    * @param content the type of ListOffsetBuilder content.
    */
  case class ListOffsetBuilder(
    offsets: String,
    content: LayoutBuilder
  ) extends LayoutBuilder {

    /**
      * Prints the structure of ListOffsetBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return string containing the offsets type and the content of ListOffsetBuilder.
      */
    override def printBuilderStructure(indent: Int): String = {
      val listOffsetContent = content.printBuilderStructure(indent)      
      s"ListOffsetBuilder<$offsets, ${listOffsetContent}>"
    }    
  }

  /**
    * Generates the RecordBuilder structure and associated strings.
    * @param fields the names of RecordBuilder fields.
    * @param contents the types of RecordBuilder contents.
    */
  case class RecordBuilder(
    fields: ListBuffer[String],
    contents: ListBuffer[LayoutBuilder],
    recordPath: String
  ) extends LayoutBuilder {
    /**
      * Prints the structure of RecordBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return strings containing the field names and the contents of RecordBuilder.
      */
    override def printBuilderStructure(indent: Int): String = {
      UserDefinedMap()
      val fieldStrings = fields.zip(contents).zipWithIndex.map { case ((field, content), i) =>
        s"${"\t" * (indent + 2)}RecordField<Field_${recordPath}::$field, ${content.printBuilderStructure(indent + 1)}>"
      }
      s"${if (indent == 0) "\nusing " + recordPath.capitalize + "BuilderType =\n\t" else ""}" +
      s"RecordBuilder<\n${fieldStrings.mkString(",\n")}\n${"\t" * (indent)}\t>"
    }

    /**
      * Prints UserDefinedMap and enum strings
      * @param indent the number of spaces to indent the structure.
      * @param builderName name of the builder.
      * @return strings containing user-defined field maps and enum strings with field ids.
      */
    def UserDefinedMap(): Unit = {
      if (!uniqueSetRecord.contains(recordPath)) {
        val mapStrings = fields.zipWithIndex.map { case (field, i) =>
          val fieldPath = field.substring(0, field.lastIndexOf("A__Z"))
          s"""{Field_${recordPath}::$field, "$field"}"""
        }
        outHdrAwkward.puts(s"enum Field_${recordPath} : std::size_t {${fields.mkString(", ")}};")
        outSrcAwkward.puts
        outSrcAwkward.puts(s"UserDefinedMap ${recordPath}_fields_map({\n\t${mapStrings.mkString(",\n\t")}});")
        uniqueSetRecord.add(recordPath)
      }
    }
  }

  /**
    * Generates the IndexedBuilder structure.
    * @param index the type of `index` buffer.
    * @param content the type of IndexedBuilder content.
    */
  case class IndexedBuilder(
    index: String,
    content: LayoutBuilder
  ) extends LayoutBuilder {

    /**
      * Prints the structure of IndexedBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return strings containing the index type and the content of IndexedBuilder.
      */
    override def printBuilderStructure(indent: Int): String = {
      val indexedContent = content.printBuilderStructure(indent)
      s"IndexedBuilder<$index, ${indexedContent}>"
    }
  }

  /**
    * Generates the IndexedOptionBuilder structure.
    * @param index the type of `index` buffer.
    * @param content the type of IndexedOptionBuilder content.
    */
  case class IndexedOptionBuilder(
    index: String,
    content: LayoutBuilder
  ) extends LayoutBuilder {

    /**
      * Prints the structure of IndexedOptionBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return strings containing the index type and the content of IndexedOptionBuilder.
      */
    override def printBuilderStructure(indent: Int): String = {
      val indexedOptionContent = content.printBuilderStructure(indent)      
      s"IndexedOptionBuilder<$index, ${indexedOptionContent}>"
    }
  }

  /**
    * Generates the UnionBuilder structure.
    * @param contents the types of UnionBuilder contents.
    */
  case class UnionBuilder(
    contents: ListBuffer[LayoutBuilder]
  ) extends LayoutBuilder {

    /**
      * Prints the structure of UnionBuilder.
      * @param indent the number of spaces to indent the structure.
      * @return strings containing the contents of UnionBuilder.
      */
    override def printBuilderStructure(indent: Int): String = {
      val unionContent = contents.zipWithIndex.map { case (content, index) =>
        s"${"\t" * (indent + 2)}${content.printBuilderStructure(indent + 1)}"
      }
      s"UnionBuilder<\n${unionContent.mkString(",\n")}\n${"\t" * (indent)}\t>"
    }
  }

  val builderMap = MutableMap.empty[String, ClassSpec]
  val checkUnion = MutableMap.empty[String, String]
  val builderTypeMap = MutableMap.empty[String, String]
  val directedMap = MutableMap.empty[String, Set[String]]
  val instancesMap = MutableMap.empty[String, Set[InstanceSpec]]

  var isRepeat = false
  var isRecord = false
  var isIndexedOption = false
  var nameList = List.empty[String]
  var typeName : String = ""
  var orderedTypes = List.empty[String]
  var currId = ""
  var layoutBuilder = RecordBuilder(ListBuffer(), ListBuffer(), "")

  sealed trait AccessMode
  case object PrivateAccess extends AccessMode
  case object PublicAccess extends AccessMode

  var accessMode: AccessMode = PublicAccess

  override def indent: String = "    "
  def typeToFileName(topClassName: String): String = topClassName
  def outFileNameSource(className: String): String = typeToFileName(className) + ".cpp"
  def outFileNameHeader(className: String): String = typeToFileName(className) + ".h"

  override def fileHeader(topClassName: String): Unit = {
    layoutBuilder = RecordBuilder(ListBuffer(), ListBuffer(), topClassName)
    outSrcHeader.puts(s"// $headerComment")
    outSrcHeader.puts

    importListSrc.addLocal(outFileNameHeader(topClassName))

    if (config.cppConfig.usePragmaOnce) {
      outHdrHeader.puts("#pragma once")
    } else {
      outHdrHeader.puts(s"#ifndef ${defineName(topClassName)}")
      outHdrHeader.puts(s"#define ${defineName(topClassName)}")
    }
    outHdrHeader.puts
    outHdrHeader.puts(s"// $headerComment")
    outHdrHeader.puts

    importListHdr.addKaitai("kaitai/kaitaistruct.h")
    importListHdr.addSystem("stdint.h")
    importListHdr.addSystem("fstream")
    importListHdr.addLocal("awkward/LayoutBuilder.h")
    importListHdr.addLocal("awkward/utils.h")

    config.cppConfig.pointers match {
      case SharedPointers | UniqueAndRawPointers =>
        importListHdr.addSystem("memory")
      case RawPointers =>
        // no extra includes
    }

    // API compatibility check
    val minVer = KSVersion.minimalRuntime.toInt
    outHdr.puts
    outHdr.puts(s"#if KAITAI_STRUCT_VERSION < ${minVer}L")
    outHdr.puts(
      "#error \"Incompatible Kaitai Struct Awkward API: version " +
        KSVersion.minimalRuntime + " or later is required\""
    )
    outHdr.puts("#endif")

    config.cppConfig.namespace.foreach { (namespace) =>
      outSrc.puts(s"namespace $namespace {")
      outSrc.inc
      outHdr.puts(s"namespace $namespace {")
      outHdr.inc
    }
    
    // Defining LayoutBuilder
    outHdrAwkward.puts
    outHdrAwkward.puts("using UserDefinedMap = std::map<std::size_t, std::string>;");
    outHdrAwkward.puts("template<class... BUILDERS>");
    outHdrAwkward.puts("using RecordBuilder = awkward::LayoutBuilder::Record<UserDefinedMap, BUILDERS...>;");
    outHdrAwkward.puts("template<std::size_t field_name, class BUILDER>");
    outHdrAwkward.puts("using RecordField = awkward::LayoutBuilder::Field<field_name, BUILDER>;");
    outHdrAwkward.puts("template<class PRIMITIVE, class BUILDER>");
    outHdrAwkward.puts("using ListOffsetBuilder = awkward::LayoutBuilder::ListOffset<PRIMITIVE, BUILDER>;");
    outHdrAwkward.puts("template<class PRIMITIVE>");
    outHdrAwkward.puts("using NumpyBuilder = awkward::LayoutBuilder::Numpy<PRIMITIVE>;");
    outHdrAwkward.puts("template<class PRIMITIVE>");
    outHdrAwkward.puts("using StringBuilder = awkward::LayoutBuilder::String<PRIMITIVE>;");
    outHdrAwkward.puts("template<class PRIMITIVE, class BUILDER>");
    outHdrAwkward.puts("using IndexedBuilder = awkward::LayoutBuilder::Indexed<PRIMITIVE, BUILDER>;");
    outHdrAwkward.puts("template<class PRIMITIVE, class BUILDER>");
    outHdrAwkward.puts("using IndexedOptionBuilder = awkward::LayoutBuilder::IndexedOption<PRIMITIVE, BUILDER>;");
    outHdrAwkward.puts("template<class... BUILDERS>");
    outHdrAwkward.puts("using UnionBuilder = awkward::LayoutBuilder::Union<int8_t, uint32_t, BUILDERS...>;");
    outHdrAwkward.puts

    checkUnion(topClassName) = ""
    builderTypeMap(topClassName) = ""
    createBuilderStructure(layoutBuilder, topClassName)
    orderedTypes = topologicalSort(directedMap.mapValues(_.toList).toMap)
  }

  override def fileFooter(topClassName: String): Unit = {
    outHdrAwkward.puts(s"${layoutBuilder.printBuilderStructure(0)};")
    outHdrAwkward.puts
    builderTypeDeclaration()
    config.cppConfig.namespace.foreach { (_) =>
      outSrc.dec
      outSrc.puts("}")
      outHdr.dec
      outHdr.puts("}")
    }

    ctypesStrings(topClassName)

    if (!config.cppConfig.usePragmaOnce) {
      outHdr.puts
      outHdr.puts(s"#endif  // ${defineName(topClassName)}")
    }
  }

  override def opaqueClassDeclaration(classSpec: ClassSpec): Unit = {
    classForwardDeclaration(classSpec.name)
    importListHdr.addLocal(outFileNameHeader(classSpec.name.head))
  }

  override def classHeader(name: List[String]): Unit = {
    val className = types2class(List(name.last))

    val extraInherits = config.cppConfig.pointers match {
      case RawPointers | UniqueAndRawPointers => ""
      case SharedPointers => s", std::enable_shared_from_this<$className>"
    }

    outHdr.puts
    outHdr.puts(s"class $className : public $kstructName$extraInherits {")
    outHdr.inc
    accessMode = PrivateAccess
    ensureMode(PublicAccess)
  }

  override def classFooter(name: List[String]): Unit = {
    outHdr.puts(s"${name.last.capitalize}BuilderType ${name.last}_builder;")   
    outHdr.dec
    outHdr.puts("};")
  }

  override def classForwardDeclaration(name: List[String]): Unit = {
    outHdr.puts(s"class ${types2class(name)};")
  }

  def importDataType(dt: DataType) = {
    dt match {
      case ut: UserType =>
        val classSpec = ut.classSpec.get
        if (classSpec.isTopLevel)
          importListSrc.addLocal(outFileNameHeader(classSpec.name.head))
      case _ => // no extra imports required
    }
  }

  override def classConstructorHeader(name: List[String], parentType: DataType, rootClassName: List[String], isHybrid: Boolean, params: List[ParamDefSpec]): Unit = {
    val (endianSuffixHdr, endianSuffixSrc)  = if (isHybrid) {
      (", int p_is_le = -1", ", int p_is_le")
    } else {
      ("", "")
    }

    val paramsArg = Utils.join(params.map { case (p) =>
      importDataType(p.dataType)
      s"${kaitaiType2NativeType(p.dataType)} ${paramName(p.id)}"
    }, "", ", ", ", ")

    val classNameBrief = types2class(List(name.last))

    // Parameter names
    val pIo = paramName(IoIdentifier)
    val pParent = paramName(ParentIdentifier)
    val pRoot = paramName(RootIdentifier)

    // Types
    val tIo = kaitaiType2NativeType(KaitaiStreamType)
    val tParent = kaitaiType2NativeType(parentType)
    val tRoot = kaitaiType2NativeType(CalcUserType(rootClassName, None))

    // Parent type might be declared somewhere else - in this case we need to include it
    importDataType(parentType)

    outHdr.puts
    outHdr.puts(s"$classNameBrief(" +
      s"${if (name.size > 1) name.last.capitalize + "BuilderType builder, " else ""}" +
      s"$paramsArg" +
      s"$tIo $pIo, " +
      s"$tParent $pParent = $nullPtr, " +
      s"$tRoot $pRoot = $nullPtr$endianSuffixHdr);"
    )

    outSrc.puts
    // Adds the constructor initiliazation for each RecordBuilder type.
    outSrc.puts(s"${types2class(name)}::$classNameBrief(" +
      s"${if (name.size > 1) name.last.capitalize + "BuilderType builder, " else ""}" +
      s"$paramsArg" +
      s"$tIo $pIo, " +
      s"$tParent $pParent, " +
      s"$tRoot $pRoot$endianSuffixSrc) : $kstructName($pIo)" + 
      s"${if (name.size > 1) ",\n\t" + name.last + "_builder(builder) {" else " {"}"
    )
    outSrc.inc
    // In shared pointers mode, this is required to be able to work with shared pointers to this
    // in a constructor. This is obviously a hack and not a good practice.
    // https://forum.libcinder.org/topic/solution-calling-shared-from-this-in-the-constructor
    if (config.cppConfig.pointers == CppRuntimeConfig.SharedPointers) {
      outSrc.puts(s"const auto weakPtrTrick = std::shared_ptr<$classNameBrief>(this, []($classNameBrief*){});")
    }

    handleAssignmentSimple(ParentIdentifier, pParent)
    handleAssignmentSimple(RootIdentifier, if (name == rootClassName) {
      config.cppConfig.pointers match {
        case RawPointers | UniqueAndRawPointers => "this"
        case SharedPointers => "shared_from_this()"
      }
    } else {
      pRoot
    })

    typeProvider.nowClass.meta.endian match {
      case Some(_: CalcEndian) | Some(InheritedEndian) =>
        ensureMode(PrivateAccess)
        outHdr.puts("int m__is_le;")
        handleAssignmentSimple(EndianIdentifier, if (isHybrid) "p_is_le" else "-1")
        ensureMode(PublicAccess)
      case _ =>
        // no _is_le variable
    }

    // Store parameters passed to us
    params.foreach((p) => handleAssignmentSimple(p.id, paramName(p.id)))
    nameList = name
  }

  override def classConstructorFooter: Unit = {
    outSrc.dec
    outSrc.puts("}")
  }

  override def classDestructorHeader(name: List[String], parentType: DataType, topClassName: List[String]): Unit = {
    ensureMode(PrivateAccess)
    outHdr.puts("void _clean_up();")
    ensureMode(PublicAccess)
    outHdr.puts(s"~${types2class(List(name.last))}();")

    outSrc.puts
    outSrc.puts(s"${types2class(name)}::~${types2class(List(name.last))}() {")
    outSrc.inc
    outSrc.puts("_clean_up();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts
    outSrc.puts(s"void ${types2class(name)}::_clean_up() {")
    outSrc.inc
  }

  override def classDestructorFooter = classConstructorFooter

  override def runRead(name: List[String]): Unit = {
    outSrc.puts
    outSrc.puts(s"${name.last}_builder.set_fields(${name.last}_fields_map);")
    val wrapToTryCatch = (config.cppConfig.pointers == CppRuntimeConfig.RawPointers);
    if (wrapToTryCatch) {
      outSrc.puts
      outSrc.puts("try {")
      outSrc.inc
    }
    outSrc.puts("_read();")
    if (wrapToTryCatch) {
      outSrc.dec
      outSrc.puts("} catch(...) {")
      outSrc.inc
      outSrc.puts("_clean_up();")
      outSrc.puts("throw;")
      outSrc.dec
      outSrc.puts("}")
    }
  }

  override def runReadCalc(): Unit = {
    outSrc.puts
    outSrc.puts("if (m__is_le == -1) {")
    outSrc.inc
    importListSrc.addKaitai("kaitai/exceptions.h")
    outSrc.puts(s"throw ${ksErrorName(UndecidedEndiannessError)}" +
      "(\"" + typeProvider.nowClass.path.mkString("/", "/", "") + "\");")
    outSrc.dec
    outSrc.puts("} else if (m__is_le == 1) {")
    outSrc.inc
    outSrc.puts("_read_le();")
    outSrc.dec
    outSrc.puts("} else {")
    outSrc.inc
    outSrc.puts("_read_be();")
    outSrc.dec
    outSrc.puts("}")
  }

  override def readHeader(endian: Option[FixedEndian], isEmpty: Boolean): Unit = {
    val suffix = endian match {
      case Some(e) => s"_${e.toSuffix}"
      case None => ""
    }

    ensureMode(if (config.autoRead) PrivateAccess else PublicAccess)

    outHdr.puts(s"void _read$suffix();")
    outSrc.puts
    outSrc.puts(s"void ${types2class(typeProvider.nowClass.name)}::_read$suffix() {")
    outSrc.inc
  }

  override def readFooter(): Unit = {
    instancesMap(nameList.last).foreach { instSpec =>
      val instName = idToStr(instSpec.id)
      val enumMapClass = instSpec match {
        case vis: ValueInstanceSpec =>
          vis.value match {
            case ebi: Ast.expr.EnumById =>
              ebi.enumName.name + "_t_map"
            case _ => ""
          }
          case _ => ""       
        }
      if (!enumMapClass.isEmpty) {
        outSrc.puts(s"auto& ${instName}_instancebuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + instName}>();")
        outSrc.puts(s"auto& ${instName}_stringbuilder = ${instName}_instancebuilder.append_index();")
        outSrc.puts(s"""${instName}_instancebuilder.set_parameters("\\"__array__\\": \\"categorical\\"");""")
        outSrc.puts(s"${instName}_stringbuilder.append(m__root->${enumMapClass}[$instName()]);")
      }
      else {
        outSrc.puts(s"auto& ${instName}_instancebuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + instName}>();")
        outSrc.puts(s"${instName}_instancebuilder.append($instName());")
      }
    }
    outSrc.dec
    outSrc.puts("}")
  }

  override def attributeDeclaration(attrName: Identifier, attrType: DataType, isNullable: Boolean): Unit = {
    ensureMode(PrivateAccess)
    outHdr.puts(s"${kaitaiType2NativeType(attrType)} ${privateMemberName(attrName)};")
    declareNullFlag(attrName, isNullable)
  }

  def ensureMode(newMode: AccessMode): Unit = {
    if (accessMode != newMode) {
      outHdr.dec
      outHdr.puts
      outHdr.puts(newMode match {
        case PrivateAccess => "private:"
        case PublicAccess => "public:"
      })
      outHdr.inc
      accessMode = newMode
    }
  }

  override def attributeReader(attrName: Identifier, attrType: DataType, isNullable: Boolean): Unit = {
    ensureMode(PublicAccess)
    outHdr.puts(s"${kaitaiType2NativeType(attrType.asNonOwning())} ${publicMemberName(attrName)}() const { return ${nonOwningPointer(attrName, attrType)}; }")
  }

  override def universalDoc(doc: DocSpec): Unit = {
    // All docstrings would be for public stuff, so it's safe to start it here
    ensureMode(PublicAccess)

    outHdr.puts
    outHdr.puts( "/**")

    doc.summary.foreach(docStr => outHdr.putsLines(" * ", docStr))

    doc.ref.foreach {
      case TextRef(text) =>
        outHdr.putsLines(" * ", s"\\sa $text")
      case UrlRef(url, text) =>
        outHdr.putsLines(" * ", s"\\sa $url $text")
    }

    outHdr.puts( " */")
  }

  override def attrInit(attr: AttrLikeSpec): Unit = {
    attr.dataTypeComposite match {
      case _: UserType | _: ArrayTypeInStream | OwnedKaitaiStreamType =>
        // data type will be pointer to user type, std::vector or stream, so we need to init it
        outSrc.puts(s"${privateMemberName(attr.id)} = $nullPtr;")
      case _ =>
        // no init required for value types
    }
  }

  override def attrDestructor(attr: AttrLikeSpec, id: Identifier): Unit = {
    val checkLazy = if (attr.isLazy) {
      Some(calculatedFlagForName(id))
    } else {
      None
    }

    val checkNull = if (attr.isNullableSwitchRaw) {
      Some(s"!${nullFlagForName(id)}")
    } else {
      None
    }

    val checks: List[String] = List(checkLazy, checkNull).flatten

    if (checks.nonEmpty) {
      outSrc.puts(s"if (${checks.mkString(" && ")}) {")
      outSrc.inc
    }

    val needRaw = this.needRaw(attr.dataType)
    val innerType = attr.dataType match {
      case st: SwitchType => st.combinedType
      case t => t
    }

    destructMember(id, innerType, attr.isArray, needRaw)

    if (checks.nonEmpty) {
      outSrc.dec
      outSrc.puts("}")
    }
  }

  def destructMember(id: Identifier, innerType: DataType, isArray: Boolean, needRaw: NeedRaw): Unit = {
    def destructWithSafeguardHeader(ptr: String): Unit = {
      outSrc.puts(s"if ($ptr) {")
      outSrc.inc
    }
    def destructWithSafeguardFooter(ptr: String): Unit = {
      outSrc.puts(s"delete $ptr; $ptr = $nullPtr;")
      outSrc.dec
      outSrc.puts("}")
    }
    def destructWithSafeguardSimple(ptr: String): Unit = {
      destructWithSafeguardHeader(ptr)
      destructWithSafeguardFooter(ptr)
    }
    if (config.cppConfig.pointers == CppRuntimeConfig.RawPointers) {
      if (isArray) {
        // raw is std::vector<string>*, no need to delete its contents, but we
        // need to clean up the vector pointer itself
        if (needRaw.level >= 1) {
          destructWithSafeguardSimple(privateMemberName(RawIdentifier(id)))

          // IO is std::vector<kstream*>*, needs destruction of both members
          // and the vector pointer itself
          if (needRaw.hasIO) {
            val ioVar = privateMemberName(IoStorageIdentifier(RawIdentifier(id)))
            destructWithSafeguardHeader(ioVar)
            destructVector(s"$kstreamName*", ioVar)
            destructWithSafeguardFooter(ioVar)
          }
        }
        if (needRaw.level >= 2) {
          // m__raw__raw_* is also std::vector<string>*, we just clean up the vector pointer
          destructWithSafeguardSimple(privateMemberName(RawIdentifier(RawIdentifier(id))))
        }

        val arrVar = privateMemberName(id)
        destructWithSafeguardHeader(arrVar)

        // main member contents
        if (needsDestruction(innerType)) {
          // C++ specific substitution: AnyType results from generic struct + raw bytes
          // so we would assume that only generic struct needs to be cleaned up
          val realType = innerType match {
            case AnyType => KaitaiStructType
            case _ => innerType
          }

          destructVector(kaitaiType2NativeType(realType), arrVar)
        }

        // main member is a std::vector of something, always needs destruction
        destructWithSafeguardFooter(arrVar)
      } else {
        // raw is just a string, no need to cleanup => we ignore `needRaw.hasRaw`

        // but needRaw.hasIO is important
        if (needRaw.hasIO)
          destructWithSafeguardSimple(privateMemberName(IoStorageIdentifier(RawIdentifier(id))))

        if (needsDestruction(innerType))
          destructWithSafeguardSimple(privateMemberName(id))
      }
    }
  }

  def needsDestruction(t: DataType): Boolean = t match {
    case _: UserType | _: ArrayTypeInStream | KaitaiStructType | AnyType => true
    case _ => false
  }

  /**
    * Generates std::vector contents destruction loop.
    * @param elType element type, i.e. XXX in `std::vector&lt;XXX&gt;`
    * @param arrVar variable name that holds pointer to std::vector
    */
  def destructVector(elType: String, arrVar: String): Unit = {
    outSrc.puts(s"for (std::vector<$elType>::iterator it = $arrVar->begin(); it != $arrVar->end(); ++it) {")
    outSrc.inc
    outSrc.puts("delete *it;")
    outSrc.dec
    outSrc.puts("}")
  }

  override def attrParseHybrid(leProc: () => Unit, beProc: () => Unit): Unit = {
    outSrc.puts("if (m__is_le == 1) {")
    outSrc.inc
    leProc()
    outSrc.dec
    outSrc.puts("} else {")
    outSrc.inc
    beProc()
    outSrc.dec
    outSrc.puts("}")
  }

  override def attrFixedContentsParse(attrName: Identifier, contents: String): Unit =
    outSrc.puts(s"${privateMemberName(attrName)} = $normalIO->ensure_fixed_contents($contents);")

  override def attrParse2(
    id: Identifier,
    dataType: DataType,
    io: String,
    rep: RepeatSpec,
    isRaw: Boolean,
    defEndian: Option[FixedEndian],
    assignTypeOpt: Option[DataType] = None
  ): Unit = {
    dataType match {
      case ut: UserType =>
        isRecord = true
        if (checkUnion.getOrElse(nameList.last + "A__Z" + ut.name.head + "__case__" + idToStr(id), "").contains("child_")) {
          outSrc.puts(s"${idToStr(id)}_unionbuilder.append_content<${checkUnion(nameList.last + "A__Z" + ut.name.head + "__case__" + idToStr(id)).split("_").last}>();")
        }
        val unionIndex = checkUnion.getOrElse(nameList.last + "A__Z" + ut.name.head + "__case__" + idToStr(id), "")
        outSrc.puts(
          s"auto& ${ut.name.head}_recordbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>()" +
          s"${if (isIndexedOption) ".content()" else ""}" +
          s"${if (isRepeat) ".content()" else ""}" +
          s"${if (unionIndex.contains("child")) ".content<" + unionIndex.split("_").last + ">()" else ""}" + 
          s";"
        )
        if (isIndexedOption) {
          typeName = ut.name.head
        }
      case _ =>
    }
    super.attrParse2(id, dataType, io, rep, isRaw, defEndian, assignTypeOpt)
    currId = idToStr(id)
    if (!privateMemberName(id).contains("m__raw")) {
      // Match case for printing the LayoutBuilder filling C++ strings in the _read() method of
      // each class based on the encountered data type and other conditions.
      dataType match {
        case Int1Type(_) | IntMultiType(_, _, _) | FloatMultiType(_, _) | BitsType(_, _) |
          _: BooleanType | CalcIntType | CalcFloatType  =>
          // Prints the C++ strings for appending the primitive data type to the Layoutbuilder.
          if (rep == NoRepeat)
            outSrc.puts(s"auto& ${idToStr(id)}_builder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>();")
          else
            outSrc.puts(s"auto& ${idToStr(id)}_builder = ${idToStr(id)}_listoffsetbuilder.content();")
          outSrc.puts(s"${idToStr(id)}_builder.append(${getRawIdExpr(id, rep)});")
        case _: StrType =>
          // Prints the C++ strings for appending the string data type to the Layoutbuilder.
          var builderName = idToStr(id)
          if (rep == NoRepeat)
            outSrc.puts(s"auto& ${builderName}_stringbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>();")
          else {
            throw new NotImplementedError("StrType with repeat is not supported yet")
            // builderName = "sub_" + builderName
            // outSrc.puts(s"auto& ${builderName}_stringbuilder = ${idToStr(id)}_stringbuilder.content();")
          }
          outSrc.puts(s"${builderName}_stringbuilder.append(${getRawIdExpr(id, rep)});")
        case _: BytesType =>
          // Prints the C++ strings for appending the bytes data type to the Layoutbuilder.
          var builderName = idToStr(id)
          if (isIndexedOption) {
            if (rep == NoRepeat)
              outSrc.puts(s"auto& ${builderName}_listoffsetbuilder = ${idToStr(id)}_indexedoptionbuilder.content();")
            else {
              builderName = "sub_" + builderName
              outSrc.puts(s"auto& ${builderName}_listoffsetbuilder = ${idToStr(id)}_listoffsetbuilder.content();")
            }
          }
          else {
            if (rep == NoRepeat)
              outSrc.puts(s"auto& ${builderName}_listoffsetbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>();")
            else {
              builderName = "sub_" + builderName
              outSrc.puts(s"auto& ${builderName}_listoffsetbuilder = ${idToStr(id)}_listoffsetbuilder.content();")
            }
          }
          outSrc.puts(s"${builderName}_listoffsetbuilder.begin_list();")
          outSrc.puts(s"auto& ${idToStr(id)}_builder = ${builderName}_listoffsetbuilder.content();")
          outSrc.puts(s"""${builderName}_listoffsetbuilder.set_parameters("\\"__array__\\": \\"bytestring\\"");""")
          outSrc.puts(s"""${idToStr(id)}_builder.set_parameters("\\"__array__\\" : \\"byte\\"");""")
          outSrc.puts(s"for (int i = 0; i < ${getRawIdExpr(id, rep)}.length(); i++) {")
          outSrc.inc
          outSrc.puts(s"${idToStr(id)}_builder.append(${getRawIdExpr(id, rep)}[i]);")
          outSrc.dec
          outSrc.puts("}")
          outSrc.puts(s"${builderName}_listoffsetbuilder.end_list();")
        case userType: UserType =>
          // Prints the C++ string to append the tags and index in the union builder buffers if a given
          // userType is a child of a UnionBuilder.
          val unionIndex = checkUnion.getOrElse(nameList.last + "A__Z" + userType.name.head + "__case__" + idToStr(id), "")
          builderTypeMap(userType.name.head) =
            s"${if (true) "using " + userType.name.head.capitalize + "BuilderType = decltype(std::declval<" + nameList.last.capitalize + 
            s"BuilderType>().content<Field_${nameList.last}::${nameList.last}A__Z${idToStr(id)}>()" +
            s"${if (isIndexedOption) ".content()" else ""}" +
            s"${if (isRepeat) ".content()" else ""}" +
            s"${if (unionIndex.contains("child")) ".content<" + unionIndex.split("_").last + ">()" else ""}" + 
            s");" else ""}"
        case enumType: EnumType =>
          var builderName = idToStr(id)
          val enumMapClass = enumType.enumSpec.get.name.last + "_t_map"
          outSrc.puts(s"auto& ${builderName}_indexbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(id)}>();")
          outSrc.puts(s"${builderName}_indexbuilder.append_index(${getRawIdExpr(id, rep)});")

          // build the enum "dictionary"
          outSrc.puts(s"auto& ${builderName}_stringbuilder = ${builderName}_indexbuilder.content();")

          outSrc.puts(s"if (${builderName}_stringbuilder.content().length() == 0) {")
          outSrc.inc
          outSrc.puts(s"""${builderName}_indexbuilder.set_parameters("\\"__array__\\": \\"categorical\\"");""")
          outSrc.puts(s"for (auto& kv: m__root->${enumMapClass} ) {")
          outSrc.inc
          outSrc.puts(s"${builderName}_stringbuilder.append(kv.second);")
          outSrc.dec
          outSrc.puts("}")
          outSrc.dec
          outSrc.puts("}")

        case _ => // do nothing
      }
      isIndexedOption = false
    }
  }

  override def attrProcess(proc: ProcessExpr, varSrc: Identifier, varDest: Identifier, rep: RepeatSpec): Unit = {
    val srcExpr = getRawIdExpr(varSrc, rep)

    val expr = proc match {
      case ProcessXor(xorValue) =>
        val procName = translator.detectType(xorValue) match {
          case _: IntType => "process_xor_one"
          case _: BytesType => "process_xor_many"
          case _ => ""
        }
        s"$kstreamName::$procName($srcExpr, ${expression(xorValue)})"
      case ProcessZlib =>
        s"$kstreamName::process_zlib($srcExpr)"
      case ProcessRotate(isLeft, rotValue) =>
        val expr = if (isLeft) {
          expression(rotValue)
        } else {
          s"8 - (${expression(rotValue)})"
        }
        s"$kstreamName::process_rotate_left($srcExpr, $expr)"
      case ProcessCustom(name, args) =>
        val procClass = name.map((x) => type2class(x)).mkString("::")
        val procName = s"_process_${idToStr(varSrc)}"

        importListSrc.addLocal(outFileNameHeader(name.last))

        val argList = args.map(expression).mkString(", ")
        var argListInParens = if (argList.nonEmpty) s"($argList)" else ""
        outSrc.puts(s"$procClass $procName$argListInParens;")
        s"$procName.decode($srcExpr)"
    }
    handleAssignment(varDest, expr, rep, false)
  }

  override def allocateIO(id: Identifier, rep: RepeatSpec): String = {
    val memberName = privateMemberName(id)
    val ioId = IoStorageIdentifier(id)

    val args = rep match {
      case RepeatUntil(_) => translator.doName(Identifier.ITERATOR2)
      case _ => getRawIdExpr(id, rep)
    }

    val newStreamRaw = s"new $kstreamName($args)"

    val ioName = rep match {
      case NoRepeat =>
        val newStream = (
          if (config.cppConfig.pointers != CppRuntimeConfig.RawPointers)
            s"${kaitaiType2NativeType(OwnedKaitaiStreamType)}($newStreamRaw)"
          else
            newStreamRaw
        )
        outSrc.puts(s"${privateMemberName(ioId)} = $newStream;")
        config.cppConfig.pointers match {
          case RawPointers =>
            privateMemberName(ioId)
          case UniqueAndRawPointers =>
            s"${privateMemberName(ioId)}.get()"
          case _ => ""
        }
      case _ =>
        val localIO = s"io_${idToStr(id)}"
        outSrc.puts(s"$kstreamName* $localIO = $newStreamRaw;")
        if (config.cppConfig.pointers == CppRuntimeConfig.UniqueAndRawPointers) {
          outSrc.puts(s"${privateMemberName(ioId)}->emplace_back($localIO);")
        } else {
          outSrc.puts(s"${privateMemberName(ioId)}->push_back($localIO);")
        }
        localIO
    }

    ioName
  }

  def getRawIdExpr(varName: Identifier, rep: RepeatSpec): String = {
    val memberName = privateMemberName(varName)
    rep match {
      case NoRepeat => memberName
      case _ => s"$memberName->at($memberName->size() - 1)"
    }
  }

  override def useIO(ioEx: Ast.expr): String = {
    outSrc.puts(s"$kstreamName *io = ${expression(ioEx)};")
    "io"
  }

  override def pushPos(io: String): Unit =
    outSrc.puts(s"std::streampos _pos = $io->pos();")

  override def seek(io: String, pos: Ast.expr): Unit =
    outSrc.puts(s"$io->seek(${expression(pos)});")

  override def popPos(io: String): Unit =
    outSrc.puts(s"$io->seek(_pos);")

  override def alignToByte(io: String): Unit =
    outSrc.puts(s"$io->align_to_byte();")

  override def instanceClear(instName: InstanceIdentifier): Unit =
    outSrc.puts(s"${calculatedFlagForName(instName)} = false;")

  override def instanceSetCalculated(instName: InstanceIdentifier): Unit =
    outSrc.puts(s"${calculatedFlagForName(instName)} = true;")

  override def condIfSetNull(instName: Identifier): Unit = {
    outSrc.puts(s"${nullFlagForName(instName)} = true;")
    // Initialize the IndexedOptionBuilder
    outSrc.puts(s"auto& ${idToStr(instName)}_indexedoptionbuilder = ${nameList.last}_builder.content<Field_${nameList.last}::${nameList.last + "A__Z" + idToStr(instName)}>();")
  }

  override def condIfSetNonNull(instName: Identifier): Unit = {
    // Appends valid index to the IndexedOptionBuilder
    outSrc.puts(s"${idToStr(instName)}_indexedoptionbuilder.append_valid();")
    outSrc.puts(s"${nullFlagForName(instName)} = false;")
  }

  override def condIfHeader(expr: Ast.expr): Unit = {
    isIndexedOption = true
    outSrc.puts(s"if (${expression(expr)}) {")
    outSrc.inc
  }

  override def condIfFooter(expr: Ast.expr): Unit = {
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts("else {")
    outSrc.inc
    // Appends invalid index to the IndexedOptionBuilder
    if (isRecord)
      outSrc.puts(s"${currId}_indexedoptionbuilder.content().set_fields(${typeName}_fields_map);")
    outSrc.puts(s"${currId}_indexedoptionbuilder.append_invalid();")
    outSrc.dec
    outSrc.puts("}") 
    outSrc.puts
    isRecord = false
  }

  override def condRepeatCommonInit(id: Identifier, dataType: DataType, needRaw: NeedRaw): Unit = {
    importListHdr.addSystem("vector")

    if (needRaw.level >= 1) {
      outSrc.puts(s"${privateMemberName(RawIdentifier(id))} = ${newVector(CalcBytesType)};")
      if (needRaw.hasIO) {
        outSrc.puts(s"${privateMemberName(IoStorageIdentifier(RawIdentifier(id)))} = ${newVector(OwnedKaitaiStreamType)};")
      }
    }
    if (needRaw.level >= 2) {
      outSrc.puts(s"${privateMemberName(RawIdentifier(RawIdentifier(id)))} = ${newVector(CalcBytesType)};")
    }
    outSrc.puts(s"${privateMemberName(id)} = ${newVector(dataType)};")
  }

  override def condRepeatEosHeader(id: Identifier, io: String, dataType: DataType): Unit = {
    outSrc.puts("{")
    outSrc.inc
    outSrc.puts("int i = 0;")
    isRepeat =  true
    currId = idToStr(id)
    // Initialize the ListOffsetBuilder for RepeatEos case and call `begin_list`
    outSrc.puts(
      s"auto& ${idToStr(id)}_listoffsetbuilder = " +
      s"${if (isIndexedOption) idToStr(id) + "_indexedoptionbuilder.content();"
      else nameList.last + "_builder.content<Field_" + nameList.last + "::" + nameList.last + "A__Z" + idToStr(id) + ">();"}"
    )
    outSrc.puts(s"${idToStr(id)}_listoffsetbuilder.begin_list();")
    outSrc.puts(s"while (!$io->is_eof()) {")
    outSrc.inc
  }

  override def handleAssignmentRepeatEos(id: Identifier, expr: String): Unit = {
    outSrc.puts(s"${privateMemberName(id)}->push_back(${stdMoveWrap(expr)});")
  }

  override def condRepeatEosFooter: Unit = {
    outSrc.puts("i++;")
    outSrc.dec
    outSrc.puts("}")
    // Calls `end_list` on the ListOffsetBuilder for RepeatEos case
    outSrc.puts(s"${currId}_listoffsetbuilder.end_list();")
    isRepeat = false
    outSrc.dec
    outSrc.puts("}")
  }

  override def condRepeatExprHeader(id: Identifier, io: String, dataType: DataType, repeatExpr: Ast.expr): Unit = {
    val lenVar = s"l_${idToStr(id)}"
    outSrc.puts(s"const int $lenVar = ${expression(repeatExpr)};")
    isRepeat =  true
    currId = idToStr(id)
    // Initialize the ListOffsetBuilder for RepeatExpr case and call `begin_list`
    outSrc.puts(
      s"auto& ${idToStr(id)}_listoffsetbuilder = " +
      s"${if (isIndexedOption) idToStr(id) + "_indexedoptionbuilder.content();"
      else nameList.last + "_builder.content<Field_" + nameList.last + "::" + nameList.last + "A__Z" + idToStr(id) + ">();"}"
    )
    outSrc.puts(s"${idToStr(id)}_listoffsetbuilder.begin_list();")
    outSrc.puts(s"for (int i = 0; i < $lenVar; i++) {")
    outSrc.inc
  }

  override def handleAssignmentRepeatExpr(id: Identifier, expr: String): Unit =
    handleAssignmentRepeatEos(id, expr)

  override def condRepeatExprFooter: Unit = {
    outSrc.dec
    outSrc.puts("}")
    // Calls `end_list` on the ListOffsetBuilder for RepeatExpr case
    outSrc.puts(s"${currId}_listoffsetbuilder.end_list();")
    isRepeat = false
  }

  override def condRepeatUntilHeader(id: Identifier, io: String, dataType: DataType, untilExpr: expr): Unit = {
    outSrc.puts("{")
    outSrc.inc
    outSrc.puts("int i = 0;")
    outSrc.puts(s"${kaitaiType2NativeType(dataType.asNonOwning())} ${translator.doName("_")};")
    isRepeat =  true
    currId = idToStr(id)
    // Initialize the ListOffsetBuilder for RepeatUntil case and call `begin_list`
    outSrc.puts(
      s"auto& ${idToStr(id)}_listoffsetbuilder = " +
      s"${if (isIndexedOption) idToStr(id) + "_indexedoptionbuilder.content();"
      else nameList.last + "_builder.content<Field_" + nameList.last + "::" + nameList.last + "A__Z" + idToStr(id) + ">();"}"
    )
    outSrc.puts(s"${idToStr(id)}_listoffsetbuilder.begin_list();")
    outSrc.puts("do {")
    outSrc.inc
  }

  private val ReStdUniquePtr = "^std::unique_ptr<(.*?)>\\((.*?)\\)$".r

  override def handleAssignmentRepeatUntil(id: Identifier, expr: String, isRaw: Boolean): Unit = {
    val (typeDecl, tempVar) = if (isRaw) {
      ("std::string ", translator.doName(Identifier.ITERATOR2))
    } else {
      ("", translator.doName(Identifier.ITERATOR))
    }

    val (wrappedTempVar, rawPtrExpr) = if (config.cppConfig.pointers == UniqueAndRawPointers) {
      expr match {
        case ReStdUniquePtr(cppClass, innerExpr) =>
          (s"std::move(std::unique_ptr<$cppClass>($tempVar))", innerExpr)
        case _ =>
          (tempVar, expr)
      }
    } else {
      (tempVar, expr)
    }

    outSrc.puts(s"$typeDecl$tempVar = $rawPtrExpr;")

    outSrc.puts(s"${privateMemberName(id)}->push_back($wrappedTempVar);")
  }

  override def condRepeatUntilFooter(id: Identifier, io: String, dataType: DataType, untilExpr: expr): Unit = {
    typeProvider._currentIteratorType = Some(dataType)
    outSrc.puts("i++;")
    outSrc.dec
    outSrc.puts(s"} while (!(${expression(untilExpr)}));")
    // Calls `end_list` on the ListOffsetBuilder for RepeatUntil case
    outSrc.puts(s"${currId}_listoffsetbuilder.end_list();")
    isRepeat = false
    outSrc.dec
    outSrc.puts("}")
  }

  override def handleAssignmentSimple(id: Identifier, expr: String): Unit = {
    outSrc.puts(s"${privateMemberName(id)} = $expr;")
  }

  override def handleAssignmentTempVar(dataType: DataType, id: String, expr: String): Unit =
    outSrc.puts(s"${kaitaiType2NativeType(dataType)} $id = $expr;")

  override def blockScopeHeader: Unit = {
    outSrc.puts("{")
    outSrc.inc
  }
  override def blockScopeFooter: Unit = {
    outSrc.dec
    outSrc.puts("}")
  }

  override def parseExpr(dataType: DataType, assignType: DataType, io: String, defEndian: Option[FixedEndian]): String = {
    dataType match {
      case t: ReadableType =>
        s"$io->read_${t.apiCall(defEndian)}()"
      case blt: BytesLimitType =>
        s"$io->read_bytes(${expression(blt.size)})"
      case _: BytesEosType =>
        s"$io->read_bytes_full()"
      case BytesTerminatedType(terminator, include, consume, eosError, _) =>
        s"$io->read_bytes_term($terminator, $include, $consume, $eosError)"
      case BitsType1(bitEndian) =>
        s"$io->read_bits_int_${bitEndian.toSuffix}(1)"
      case BitsType(width: Int, bitEndian) =>
        s"$io->read_bits_int_${bitEndian.toSuffix}($width)"
      case t: UserType =>
        val addParams = s"${t.name.head}_recordbuilder, " + Utils.join(t.args.map((a) => translator.translate(a)), "", ", ", ", ")
        val addArgs = if (t.isOpaque) {
          ""
        } else {
          val parent = t.forcedParent match {
            case Some(USER_TYPE_NO_PARENT) => nullPtr
            case Some(fp) => translator.translate(fp)
            case None =>
              config.cppConfig.pointers match {
                case RawPointers | UniqueAndRawPointers => "this"
                case SharedPointers => s"shared_from_this()"
              }
          }
          val addEndian = t.classSpec.get.meta.endian match {
            case Some(InheritedEndian) => ", m__is_le"
            case _ => ""
          }
          s", $parent, ${privateMemberName(RootIdentifier)}$addEndian"
        }
        config.cppConfig.pointers match {
          case RawPointers =>
            s"new ${types2class(t.name)}($addParams$io$addArgs)"
          case SharedPointers =>
            s"std::make_shared<${types2class(t.name)}>($addParams$io$addArgs)"
          case UniqueAndRawPointers =>
            // C++14
            //s"std::make_unique<${types2class(t.name)}>($addParams$io$addArgs)"
            s"std::unique_ptr<${types2class(t.name)}>(new ${types2class(t.name)}($addParams$io$addArgs))"
        }
      case _ => ""
    }
  }

  def newVector(elType: DataType): String = {
    val cppElType = kaitaiType2NativeType(elType)
    config.cppConfig.pointers match {
      case RawPointers =>
        s"new std::vector<$cppElType>()"
      case UniqueAndRawPointers =>
        s"std::unique_ptr<std::vector<$cppElType>>(new std::vector<$cppElType>())"
        // TODO: C++14 with std::make_unique
      case _ => ""
    }
  }

  override def bytesPadTermExpr(expr0: String, padRight: Option[Int], terminator: Option[Int], include: Boolean) = {
    val expr1 = padRight match {
      case Some(padByte) => s"$kstreamName::bytes_strip_right($expr0, $padByte)"
      case None => expr0
    }
    val expr2 = terminator match {
      case Some(term) => s"$kstreamName::bytes_terminate($expr1, $term, $include)"
      case None => expr1
    }
    expr2
  }

  override def userTypeDebugRead(id: String, dataType: DataType, assignType: DataType): Unit = {
    val expr = if (assignType != dataType) {
      s"static_cast<${kaitaiType2NativeType(dataType)}>($id)"
    } else {
      id
    }
    outSrc.puts(s"$expr->_read();")
  }

  override def switchRequiresIfs(onType: DataType): Boolean = onType match {
    case _: IntType | _: EnumType => false
    case _ => true
  }

  //<editor-fold desc="switching: true version">

  override def switchStart(id: Identifier, on: Ast.expr): Unit = {
    // Initialize the UnionBuilder
    outSrc.puts(
      s"auto& ${idToStr(id)}_unionbuilder = " +
      s"${if (isRepeat) idToStr(id) + "_listoffsetbuilder.content();"
      else nameList.last + "_builder.content<Field_" + nameList.last + "::" + nameList.last + "A__Z" + idToStr(id) + ">();"}"
    )
    outSrc.puts(s"switch (${expression(on)}) {")
  }

  override def switchCaseFirstStart(condition: Ast.expr): Unit = {
    outSrc.puts(s"case ${expression(condition)}: {")
    outSrc.inc
  }

  override def switchCaseStart(condition: Ast.expr): Unit = {
    outSrc.puts(s"case ${expression(condition)}: {")
    outSrc.inc
  }

  override def switchCaseEnd(): Unit = {
    outSrc.puts("break;")
    outSrc.dec
    outSrc.puts("}")
  }

  override def switchElseStart(): Unit = {
    outSrc.puts("default: {")
    outSrc.inc
  }

  override def switchEnd(): Unit =
    outSrc.puts("}")

  //</editor-fold>

  //<editor-fold desc="switching: emulation with ifs">

  override def switchIfStart(id: Identifier, on: Ast.expr, onType: DataType): Unit = {
    outSrc.puts("{")
    outSrc.inc
    outSrc.puts(s"${kaitaiType2NativeType(onType)} on = ${expression(on)};")
  }

  override def switchIfCaseFirstStart(condition: Ast.expr): Unit = {
    outSrc.puts(s"if (on == ${expression(condition)}) {")
    outSrc.inc
  }

  override def switchIfCaseStart(condition: Ast.expr): Unit = {
    outSrc.puts(s"else if (on == ${expression(condition)}) {")
    outSrc.inc
  }

  override def switchIfCaseEnd(): Unit = {
    outSrc.dec
    outSrc.puts("}")
  }

  override def switchIfElseStart(): Unit = {
    outSrc.puts("else {")
    outSrc.inc
  }

  override def switchIfEnd(): Unit = {
    outSrc.dec
    outSrc.puts("}")
  }

  //</editor-fold>

  override def switchBytesOnlyAsRaw = true

  override def instanceDeclaration(attrName: InstanceIdentifier, attrType: DataType, isNullable: Boolean): Unit = {
    ensureMode(PrivateAccess)
    outHdr.puts(s"bool ${calculatedFlagForName(attrName)};")
    outHdr.puts(s"${kaitaiType2NativeType(attrType)} ${privateMemberName(attrName)};")
    declareNullFlag(attrName, isNullable)
  }

  override def instanceHeader(className: List[String], instName: InstanceIdentifier, dataType: DataType, isNullable: Boolean): Unit = {
    ensureMode(PublicAccess)
    outHdr.puts(s"${kaitaiType2NativeType(dataType.asNonOwning())} ${publicMemberName(instName)}();")

    outSrc.puts
    outSrc.puts(s"${kaitaiType2NativeType(dataType.asNonOwning(), true)} ${types2class(className)}::${publicMemberName(instName)}() {")
    outSrc.inc
  }

  override def instanceFooter: Unit = {
    outSrc.dec
    outSrc.puts("}")
  }

  override def instanceCheckCacheAndReturn(instName: InstanceIdentifier, dataType: DataType): Unit = {
    outSrc.puts(s"if (${calculatedFlagForName(instName)}) {")
    outSrc.inc
    instanceReturn(instName, dataType)
    outSrc.dec
    outSrc.puts("}")
  }

  override def instanceReturn(instName: InstanceIdentifier, attrType: DataType): Unit = {
    outSrc.puts(s"return ${nonOwningPointer(instName, attrType)};")
    }

  override def instanceCalculate(instName: Identifier, dataType: DataType, value: Ast.expr): Unit = {
    if (config.readStoresPos)
      attrDebugStart(instName, dataType, None, NoRepeat)
    val valExpr = expression(value)
    val isOwningInExpr = dataType match {
      case ct: ComplexDataType => ct.isOwningInExpr
      case _ => false
    }
    handleAssignmentSimple(instName, if (isOwningInExpr) s"$valExpr.get()" else valExpr)
  }

  override def enumDeclaration(curClass: List[String], enumName: String, enumColl: Seq[(Long, EnumValueSpec)]): Unit = {
    val enumClass = types2class(List(enumName))

    outHdr.puts
    outHdr.puts(s"enum $enumClass {")
    outHdr.inc

    val maxEnum = enumColl.map(_._1).max

    val EmptyStringEnumValueSpec = EnumValueSpec("null", DocSpec(None, List()))

    // loop from 0 to maxEnum
    // create enumColl2 with all the values from enumColl
    // but with the missing values filled with EmptyStringEnumValueSpec

    val enumColl2 = (0L to maxEnum).map { i =>
      enumColl.find(_._1 == i).getOrElse((i, EmptyStringEnumValueSpec))
    }

    if (enumColl2.size > 1) {
      enumColl2.dropRight(1).foreach { case (id, label) =>
        outHdr.puts(
          s"${value2Const(enumName, label.name)} = ${translator.doIntLiteral(id)},"
        )
      }
    }
    enumColl2.last match {
      case (id, label) =>
        outHdr.puts(
          s"${value2Const(enumName, label.name)} = ${translator.doIntLiteral(id)}"
        )
    }

    outHdr.dec
    outHdr.puts("};")

    outHdr.puts
    outHdr.puts(s"std::map<int, std::string> ${enumClass}_map {")
    outHdr.inc
    if (enumColl2.size > 1) {
      enumColl2.dropRight(1).foreach { case (id, label) =>
        outHdr.puts(s"""{${translator.doIntLiteral(id)}, \"${label.name}\"},""")
      }
    }
    enumColl2.last match {
      case (id, label) =>
        outHdr.puts(s"""{${translator.doIntLiteral(id)}, \"${label.name}\"},""")
    }
    outHdr.dec
    outHdr.puts("};")
  }

  override def classToString(toStringExpr: Ast.expr): Unit = {
    ensureMode(PublicAccess)
    // _to_string() method
    outHdr.puts(s"std::string _to_string() const;")
    outSrc.puts
    outSrc.puts(s"std::string ${types2class(typeProvider.nowClass.name)}::_to_string() const {")
    outSrc.inc
    outSrc.puts(s"return ${translator.translate(toStringExpr)};")
    outSrc.dec
    outSrc.puts("}")

    // operator<< that trivially calls ._to_string()
    outHdr.puts(s"friend std::ostream& operator<<(std::ostream& os, const ${types2class(typeProvider.nowClass.name)}& obj);")
    outSrc.puts
    outSrc.puts(s"std::ostream& operator<<(std::ostream& os, const ${types2class(typeProvider.nowClass.name)}& obj) {")
    outSrc.inc
    outSrc.puts("os << obj._to_string();")
    outSrc.puts("return os;")
    outSrc.dec
    outSrc.puts("}")
  }

  def value2Const(enumName: String, label: String) = Utils.upperUnderscoreCase(enumName + "_" + label)

  def defineName(className: String) = Utils.upperUnderscoreCase(className) + "_H_"

  /**
    * Returns name of a member that stores "calculated flag" for a given lazy
    * attribute. That is, if it's true, then calculation have already taken
    * place and we need to return already calculated member in a getter, or,
    * if it's false, we need to calculate / parse it first.
    * @param ksName attribute ID
    * @return calculated flag member name associated with it
    */
  def calculatedFlagForName(ksName: Identifier) =
    s"f_${idToStr(ksName)}"

  /**
    * Returns name of a member that stores "null flag" for a given attribute,
    * that is, if it's true, then associated attribute is null.
    * @param ksName attribute ID
    * @return null flag member name associated with it
    */
  def nullFlagForName(ksName: Identifier) =
    s"n_${idToStr(ksName)}"

  override def idToStr(id: Identifier): String = AwkwardCompiler.idToStr(id)

  override def publicMemberName(id: Identifier): String = AwkwardCompiler.publicMemberName(id)

  override def privateMemberName(id: Identifier): String = s"m_${idToStr(id)}"


  override def localTemporaryName(id: Identifier): String = s"_t_${idToStr(id)}"

  override def paramName(id: Identifier): String = s"p_${idToStr(id)}"

  def declareNullFlag(attrName: Identifier, isNullable: Boolean) = {
    if (isNullable) {
      outHdr.puts(s"bool ${nullFlagForName(attrName)};")
      ensureMode(PublicAccess)
      outHdr.puts(s"bool _is_null_${idToStr(attrName)}() { ${publicMemberName(attrName)}(); return ${nullFlagForName(attrName)}; };")
      ensureMode(PrivateAccess)
    }
  }

  override def type2class(className: String): String = AwkwardCompiler.type2class(className)

  def types2type(types: String): String = {
    val lastIndex = types.lastIndexOf(":")

    if (lastIndex != -1)
      types.substring(lastIndex + 1).dropRight(3)
    else
      types.dropRight(3)
  }

  def kaitaiType2NativeType(attrType: DataType, absolute: Boolean = false): String = {
    AwkwardCompiler.kaitaiType2NativeType(config.cppConfig, attrType, absolute)
  }

  /**
    * creates the builder map which maps the ClassSpec information to the path.
    * @param curClass the current ClassCpec
    * @param firstSpec the first ClassSpec
    * @param path current path string
    */
  override def createBuilderMap(curClass: ClassSpec, firstSpec: ClassSpec) {
    directedMap.getOrElseUpdate(curClass.name.last, Set())
    builderMap(curClass.name.last) = curClass
    curClass.seq.foreach { el =>
      el.dataType match {
        case userType: UserType =>
          directedMap(curClass.name.last) += userType.name.head
          createBuilderMap(firstSpec.types(userType.name.head), firstSpec)
        case switchType: SwitchType =>
          switchType.cases.values.foreach {
            case ut: UserType =>
              directedMap(curClass.name.last) += ut.name.head
              createBuilderMap(firstSpec.types(ut.name.head), firstSpec)
            case _ =>
          }
        case _ =>
      }
    }
  }

  /**
    * Uses the information in builderMap to create the builder structure based on the data type.
    * @param builder the current RecordBuilder to be filled.
    * @param key the path to search in the builderMap.
    */
  def createBuilderStructure(builder: RecordBuilder, key: String): Unit = {
    builderMap(key) match { case cs: ClassSpec =>
      cs.seq.foreach { el =>
        el.dataType match {
          case userType: UserType =>
            // for UserType, RecordBuilder will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            var builderContent = checkRepeat(el.cond.repeat, RecordBuilder(ListBuffer(), ListBuffer(), userType.name.head))
            builder.contents += checkOption(el, builderContent)
            builder.contents.last match {
              case recordBuilder: AwkwardCompiler.this.RecordBuilder =>
                createBuilderStructure(recordBuilder, userType.name.head)
              case listOffsetBuilder: AwkwardCompiler.this.ListOffsetBuilder =>
                listOffsetBuilder.content match {
                  case rb: AwkwardCompiler.this.RecordBuilder =>
                    createBuilderStructure(rb, userType.name.head)
                  case ib: AwkwardCompiler.this.IndexedOptionBuilder =>
                    createBuilderStructure(ib.content.asInstanceOf[RecordBuilder], userType.name.head)
                  case _ =>
                }
              case indexedOptionBuilder: AwkwardCompiler.this.IndexedOptionBuilder =>
                createBuilderStructure(indexedOptionBuilder.content.asInstanceOf[RecordBuilder], userType.name.head)
              case unsupportedBuilder => throw new UnsupportedOperationException(s"Unsupported builder: $unsupportedBuilder")
            }
          case switchType: SwitchType =>
            // for SwitchType, UnionBuilder will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            var builderContent = checkRepeat(el.cond.repeat, UnionBuilder(ListBuffer()))
            builder.contents += checkOption(el,builderContent)
            checkUnion(cs.name.last + "A__Z" + idToStr(el.id)) = "parent"
            val unionBuilder = builder.contents.last match {
              case lb: AwkwardCompiler.this.ListOffsetBuilder => lb.content.asInstanceOf[UnionBuilder]
              case ub: AwkwardCompiler.this.UnionBuilder => ub.asInstanceOf[UnionBuilder]
            }
            switchType.cases.values.zipWithIndex.foreach { case (dataType, index) =>
              dataType match {
                case ut: UserType =>
                  checkUnion(cs.name.last + "A__Z" + ut.name.head + "__case__" + idToStr(el.id)) = "child_" + index
                  var builderContent = checkRepeat(NoRepeat, RecordBuilder(ListBuffer(), ListBuffer(), ut.name.head))
                  unionBuilder.contents += checkOption(el, builderContent)

                  unionBuilder.contents.last match {
                    case recordBuilder: AwkwardCompiler.this.RecordBuilder =>
                      createBuilderStructure(recordBuilder, ut.name.head)
                    case listOffsetBuilder: AwkwardCompiler.this.ListOffsetBuilder =>
                      listOffsetBuilder.content match {
                        case rb: AwkwardCompiler.this.RecordBuilder =>
                          createBuilderStructure(rb, ut.name.head)
                        case ib: AwkwardCompiler.this.IndexedOptionBuilder =>
                          createBuilderStructure(ib.content.asInstanceOf[RecordBuilder], ut.name.head)
                        case _ =>
                      }
                    case indexedOptionBuilder: AwkwardCompiler.this.IndexedOptionBuilder =>
                      createBuilderStructure(indexedOptionBuilder.content.asInstanceOf[RecordBuilder], ut.name.head)
                    case unsupportedBuilder => throw new UnsupportedOperationException(s"Unsupported builder: $unsupportedBuilder")
                  }
                case _ =>
              }
            }
          case Int1Type(_) | IntMultiType(_, _, _) | FloatMultiType(_, _) | BitsType(_, _) |
           _: BooleanType | CalcIntType | CalcFloatType  =>
            // for primitive types, NumpyBuilder will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            var builderContent = checkRepeat(el.cond.repeat, NumpyBuilder(kaitaiType2NativeType(el.dataType)))
            builder.contents += checkOption(el, builderContent)
          case _: StrType =>
            // for strings, StringBuilder(int64_t) will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            var builderContent = checkRepeat(el.cond.repeat, StringBuilder("int64_t"))
            builder.contents += checkOption(el, builderContent)
          case _: BytesType =>
            // for bytes, ListOffsetBuilder(int64_t, NumpyBuilder(uint8_t)) will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            var builderContent = checkRepeat(el.cond.repeat, ListOffsetBuilder("int64_t", NumpyBuilder("uint8_t")))
            builder.contents += checkOption(el, builderContent)
          case enumType: EnumType =>
            // for enum types, NumpyBuilder of the given type will be generated.
            builder.fields += cs.name.last + "A__Z" + idToStr(el.id)
            builder.contents += IndexedBuilder(kaitaiType2NativeType(enumType.basedOn), StringBuilder("int64_t") )
          case _ => throw new UnsupportedOperationException(s"Unsupported data type: ${el.dataType}")
        }
      }

      instancesMap.getOrElseUpdate(cs.name.last, Set())
      // for adding the builders for the instances.
      cs.instances.foreach { case (instName, instSpec) =>
        instancesMap(cs.name.last) += instSpec
        builder.fields += cs.name.last + "A__Z" + idToStr(instName)
        instSpec.dataTypeComposite.asNonOwning() match {
          case et: EnumType =>
            // for enum cases of the instances.
            builder.contents += IndexedBuilder(kaitaiType2NativeType(et.basedOn), StringBuilder("int64_t") )
          case _ => builder.contents += NumpyBuilder(kaitaiType2NativeType(instSpec.dataTypeComposite.asNonOwning()))
        }
      }
      case _ =>
    }
  }

  /**
    * Checks the repeat condition for adding ListOffsetBuilder.
    * @param rep RepeatSpec of the identifier
    * @param builderContent last content of the current builder.
    * @return the builder content obtained after checking the conditions.
    */
  def checkRepeat(rep: RepeatSpec, builderContent: LayoutBuilder): LayoutBuilder = {
    rep match {
      case NoRepeat => builderContent
      case _ => ListOffsetBuilder("int64_t", builderContent)
    }
  }

  /**
    * Checks the repeat condition for adding IndexedOptionBuilder.
    * @param spec the AttrSpec of the current Class.
    * @param builderContent last content of the current builder.
    * @return the builder content obtained after checking the conditions.
    */
  def checkOption(spec: AttrSpec, builderContent: LayoutBuilder): LayoutBuilder = {
    if (spec.cond.ifExpr.isDefined) {
      IndexedOptionBuilder("int64_t", builderContent)
    }
    else {
      builderContent
    }
  }

  /**
    * Topologically sorts and converts the map into list of types.
    * @param graph directed map of types 
    * @return sorted list of stypes
    */
  def topologicalSort(graph: Map[String, List[String]]): List[String] = {
    val inDegree = MutableMap[String, Int]().withDefaultValue(0)
    val stack = Stack[String]()
    val result = ListBuffer[String]()

    graph.values.flatten.foreach { node =>
      inDegree(node) += 1
    }

    graph.keys.foreach { node =>
      if (inDegree(node) == 0) {
        stack.push(node)
      }
    }

    while (stack.nonEmpty) {
      val current = stack.pop()
      result += current

      graph(current).foreach { neighbor =>
        inDegree(neighbor) -= 1
        if (inDegree(neighbor) == 0) {
          stack.push(neighbor)
        }
      }
    }
    result.toList
  }

  /**
    * Prints the builder type declarations for each class recursively based on the order of types.
    */
  def builderTypeDeclaration(): Unit = {
    for (childClass <- orderedTypes) {
      outHdrAwkward.puts(builderTypeMap(childClass))
    }
  }

  /**
    * Generates the C/C++ strings for methods that load the raw
    * file and fill the Awkward buffers. These methods are accessed
    * from Python via ctypes
    * @param topClassName name of the root class
    */
  def ctypesStrings(topClassName: String): Unit = {
    val builderType = s"${topClassName.capitalize}BuilderType"
    
    outHdr.puts
    outHdr.puts(s"#ifndef USE_${topClassName.toUpperCase()}_")
    outHdr.puts(s"#define USE_${topClassName.toUpperCase()}_")
    outSrc.puts
    outSrc.puts(s"#ifdef USE_${topClassName.toUpperCase()}_")

    outSrc.puts
    outSrc.puts(s"std::map<std::string, $builderType*> builder_map;")
    outSrc.puts(s"std::vector<std::string>* builder_keys;")
    outHdr.puts
    outHdr.puts(s"$builderType* load(std::string file_path);")
    outHdr.puts
    outSrc.puts
    outSrc.puts(s"$builderType* load(std::string file_path) {")
    outSrc.inc
    outSrc.puts("std::ifstream infile(file_path, std::ifstream::binary);")
    outSrc.puts("kaitai::kstream ks(&infile);")
    outSrc.puts(s"builder_keys = new std::vector<std::string>();")
    outSrc.puts(s"${topClassName}_t* obj = new ${topClassName}_t(&ks);")
    outSrc.puts(s"builder_map[file_path] = &(obj->${topClassName}_builder);")
    outSrc.puts("return builder_map[file_path];")
    outSrc.dec
    outSrc.puts(s"}")
    outSrc.puts

    outHdr.puts(s"""extern "C" {""")
    outHdr.puts
    outHdr.inc
    outSrc.puts(s"""extern "C" {""")
    outSrc.puts
    outSrc.inc

    outHdr.puts("struct Result {")
    outHdr.inc
    outHdr.puts("void* builder;")
    outHdr.puts("const char* error_message;")
    outHdr.dec
    outHdr.puts("};")
    outHdr.puts

    outHdr.puts("Result fill(const char* file_path);")
    outHdr.puts
    outSrc.puts("Result fill(const char* file_path) {")
    outSrc.inc
    outSrc.puts("Result result;")
    outSrc.puts("std::string error_message;")
    outSrc.puts(s"$builderType* builder = load(file_path);")
    outSrc.puts("bool is_valid = builder->is_valid(error_message);")
    outSrc.puts("if (is_valid) {")
    outSrc.inc
    outSrc.puts("result.builder = builder;")
    outSrc.puts("result.error_message = NULL;")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts("else {")
    outSrc.inc
    outSrc.puts("result.builder = NULL;")
    outSrc.puts("builder_keys->push_back(error_message);")
    outSrc.puts("result.error_message = builder_keys->back().c_str();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts("return result;")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("const char* form(void* builder);")
    outHdr.puts
    outSrc.puts("const char* form(void* builder) {")
    outSrc.inc
    outSrc.puts(s"builder_keys->push_back(reinterpret_cast<$builderType*>(builder)->form());")
    outSrc.puts(s"return builder_keys->back().c_str();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("int64_t length(void* builder);")
    outHdr.puts
    outSrc.puts("int64_t length(void* builder) {")
    outSrc.inc
    outSrc.puts(s"return reinterpret_cast<$builderType*>(builder)->length();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("int64_t num_buffers(void* builder);")
    outHdr.puts
    outSrc.puts("int64_t num_buffers(void* builder) {")
    outSrc.inc
    outSrc.puts(s"return awkward::num_buffers_helper(reinterpret_cast<$builderType*>(builder));")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("const char* buffer_name(void* builder, int64_t index);")
    outHdr.puts
    outSrc.puts("const char* buffer_name(void* builder, int64_t index) {")
    outSrc.inc
    outSrc.puts(s"builder_keys->push_back(awkward::buffer_name_helper(reinterpret_cast<$builderType*>(builder))[index]);")
    outSrc.puts(s"return builder_keys->back().c_str();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("int64_t buffer_size(void* builder, int64_t index);")
    outHdr.puts
    outSrc.puts("int64_t buffer_size(void* builder, int64_t index) {")
    outSrc.inc
    outSrc.puts(s"return awkward::buffer_size_helper(reinterpret_cast<$builderType*>(builder))[index];")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("void copy_into(const char* name, void* from_builder, void* to_buffer, int64_t index);")
    outHdr.puts
    outSrc.puts("void copy_into(const char* name, void* from_builder, void* to_buffer, int64_t index) {")
    outSrc.inc
    outSrc.puts(s"reinterpret_cast<$builderType*>(from_builder)->to_buffer(to_buffer, name);")
    outSrc.dec
    outSrc.puts("}")
    outSrc.puts

    outHdr.puts("void deallocate(void* builder);")
    outHdr.dec
    outSrc.puts("void deallocate(void* builder) {")
    outSrc.inc
    outSrc.puts(s"delete builder_keys;")
    outSrc.puts(s"reinterpret_cast<$builderType*>(builder)->clear();")
    outSrc.dec
    outSrc.puts("}")
    outSrc.dec

    outHdr.puts("}")
    outHdr.puts
    outHdr.puts(s"#endif // USE_${topClassName.toUpperCase()}_")
    outHdr.puts
    outSrc.puts("}")
    outSrc.puts
    outSrc.puts(s"#endif // USE_${topClassName.toUpperCase()}_")
    outSrc.puts
  }

  def nullPtr: String = config.cppConfig.pointers match {
    case RawPointers => "0"
    case SharedPointers | UniqueAndRawPointers => "nullptr"
  }

  def nonOwningPointer(attrName: Identifier, attrType: DataType): String = {
    config.cppConfig.pointers match {
      case RawPointers =>
        privateMemberName(attrName)
      case UniqueAndRawPointers =>
        attrType match {
          case st: SwitchType =>
            nonOwningPointer(attrName, combineSwitchType(st))
          case t: ComplexDataType =>
            if (t.isOwning) {
              s"${privateMemberName(attrName)}.get()"
            } else {
              privateMemberName(attrName)
            }
          case _ =>
            privateMemberName(attrName)
        }
      case _ => ""
    }
  }

  def stdMoveWrap(expr: String): String = config.cppConfig.pointers match {
    case UniqueAndRawPointers => s"std::move($expr)"
    case _ => expr
  }

  override def ksErrorName(err: KSError): String = err match {
    case EndOfStreamError => "std::ifstream::failure"
    case UndecidedEndiannessError => "kaitai::undecided_endianness_error"
    case ConversionError => "std::invalid_argument"
    case validationErr: ValidationError =>
      val cppType = kaitaiType2NativeType(validationErr.dt, true)
      val cppErrName = validationErr match {
        case _: ValidationNotEqualError => "validation_not_equal_error"
        case _: ValidationLessThanError => "validation_less_than_error"
        case _: ValidationGreaterThanError => "validation_greater_than_error"
        case _: ValidationNotAnyOfError => "validation_not_any_of_error"
        case _: ValidationExprError => "validation_expr_error"
      }
      s"kaitai::$cppErrName<$cppType>"
  }

  override def attrValidateExpr(
    attrId: Identifier,
    attrType: DataType,
    checkExpr: Ast.expr,
    err: KSError,
    errArgs: List[Ast.expr]
  ): Unit = {
    val errArgsStr = errArgs.map(translator.translate).mkString(", ")
    importListSrc.addKaitai("kaitai/exceptions.h")
    outSrc.puts(s"if (!(${translator.translate(checkExpr)})) {")
    outSrc.inc
    outSrc.puts(s"throw ${ksErrorName(err)}($errArgsStr);")
    outSrc.dec
    outSrc.puts("}")
  }
}

object AwkwardCompiler extends LanguageCompilerStatic
  with StreamStructNames {
  override def getCompiler(
    tp: ClassTypeProvider,
    config: RuntimeConfig
  ): LanguageCompiler = new AwkwardCompiler(tp, config)

  def idToStr(id: Identifier): String =
    id match {
      case SpecialIdentifier(name) => Utils.lowerUnderscoreCase(name)
      case NamedIdentifier(name) => Utils.lowerUnderscoreCase(name)
      case NumberedIdentifier(idx) => s"_${NumberedIdentifier.TEMPLATE}$idx"
      case InstanceIdentifier(name) => Utils.lowerUnderscoreCase(name)
      case RawIdentifier(inner) => s"_raw_${idToStr(inner)}"
      case IoStorageIdentifier(inner) => s"_io_${idToStr(inner)}"
    }

  def publicMemberName(id: Identifier): String = idToStr(id)

  override def kstructName = "kaitai::kstruct"
  override def kstreamName = "kaitai::kstream"

  def kaitaiType2NativeType(config: CppRuntimeConfig, attrType: DataType, absolute: Boolean = false): String = {
    attrType match {
      case Int1Type(false) => "uint8_t"
      case IntMultiType(false, Width2, _) => "uint16_t"
      case IntMultiType(false, Width4, _) => "uint32_t"
      case IntMultiType(false, Width8, _) => "uint64_t"

      case Int1Type(true) => "int8_t"
      case IntMultiType(true, Width2, _) => "int16_t"
      case IntMultiType(true, Width4, _) => "int32_t"
      case IntMultiType(true, Width8, _) => "int64_t"

      case FloatMultiType(Width4, _) => "float"
      case FloatMultiType(Width8, _) => "double"

      case BitsType(_, _) => "uint64_t"

      case _: BooleanType => "bool"
      case CalcIntType => "int32_t"
      case CalcFloatType => "double"

      case _: StrType => "std::string"
      case _: BytesType => "std::string"

      case t: UserType =>
        val typeStr = types2class(if (absolute) {
          t.classSpec.get.name
        } else {
          t.name
        })
        config.pointers match {
          case RawPointers => s"$typeStr*"
          case SharedPointers => s"std::shared_ptr<$typeStr>"
          case UniqueAndRawPointers =>
            if (t.isOwning) s"std::unique_ptr<$typeStr>" else s"$typeStr*"
        }

      case t: EnumType =>
        types2class(if (absolute) {
          t.enumSpec.get.name
        } else {
          t.name
        })

      case ArrayTypeInStream(inType) => config.pointers match {
        case RawPointers => s"std::vector<${kaitaiType2NativeType(config, inType, absolute)}>*"
        case UniqueAndRawPointers => s"std::unique_ptr<std::vector<${kaitaiType2NativeType(config, inType, absolute)}>>"
        case _ => ""
      }
      case CalcArrayType(inType, _) => s"std::vector<${kaitaiType2NativeType(config, inType, absolute)}>*"
      case OwnedKaitaiStreamType => config.pointers match {
        case RawPointers => s"$kstreamName*"
        case UniqueAndRawPointers => s"std::unique_ptr<$kstreamName>"
        case _ => ""
      }
      case KaitaiStreamType => s"$kstreamName*"
      case KaitaiStructType => config.pointers match {
        case RawPointers => s"$kstructName*"
        case SharedPointers => s"std::shared_ptr<$kstructName>"
        case UniqueAndRawPointers => s"std::unique_ptr<$kstructName>"
      }
      case CalcKaitaiStructType(_) => config.pointers match {
        case RawPointers => s"$kstructName*"
        case SharedPointers => s"std::shared_ptr<$kstructName>"
        case UniqueAndRawPointers => s"$kstructName*"
      }

      case st: SwitchType =>
        kaitaiType2NativeType(config, combineSwitchType(st), absolute)
      case _ => ""
    }
  }

  /**
    * C++ does not have a concept of AnyType, and common use case "lots of
    * incompatible UserTypes for cases + 1 BytesType for else" combined would
    * result in exactly AnyType - so we try extra hard to avoid that here with
    * this pre-filtering. In C++, "else" case with raw byte array would
    * be available through _raw_* attribute anyway.
    *
    * @param st switch type to combine into one overall type
    * @return
    */
  def combineSwitchType(st: SwitchType): DataType = {
    val ct1 = TypeDetector.combineTypes(
      st.cases.filterNot {
        case (caseExpr, _: BytesType) => caseExpr == SwitchType.ELSE_CONST
        case _ => false
      }.values
    )
    if (st.isOwning) {
      ct1
    } else {
      ct1.asNonOwning()
    }
  }

  def types2class(typeName: Ast.typeId) = {
    typeName.names.map(type2class).mkString(
      if (typeName.absolute) "::" else "",
      "::",
      ""
    )
  }

  def types2class(components: List[String]) =
    components.map(type2class).mkString("::")

  def type2class(name: String) = Utils.lowerUnderscoreCase(name) + "_t"
}
