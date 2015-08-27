#include "mqo.h"
#include "linereader.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>

namespace meshio {
  namespace mqo {

    //! Tokenizer
    struct DELIMITER
    {
      bool operator()(char c)
      {
        switch(c)
        {
          case ' ':
          case '\t':
          case '(':
          case ')':
            return true;
          default:
            return false;
        }
      }
    };
    typedef LineSplitter<DELIMITER> SPLITTER;


    //! ŽÀ‘•
    class Implementation
    {
      Scene &scene;
      std::vector<Material> &materials;
      std::vector<Object> &objects;

    public:
      Implementation(Scene &_scene, std::vector<Material> &_materials,
          std::vector<Object> &_objects)
        : scene(_scene), materials(_materials), objects(_objects)
      {}

      template<class READER> bool 
        parse(READER reader)
        {
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            SPLITTER splitter(line);
            cstr key=splitter.get();
            if(key=="Scene"){
              if(!readSceneChunk(reader)){
                return false;
              }
            }
            else if(key=="Material"){
              if(!readMaterialChunk(reader, splitter.getInt())){
                return false;
              }
            }
            else if(key=="Object"){
              if(!readObjectChunk(reader, splitter.getQuated())){
                return false;
              }
            }
            else if(key=="Eof"){
              if(materials.empty()){
                // fallback
                //materials.push_back(Material());
              }
              return true;
            }
          }
          std::cout << "not found 'EOF'" << std::endl;
          return true;
        }


    private:
      template<class READER> bool 
        readObjectChunk(READER &reader, cstr name)
        {
          objects.push_back(Object());
          Object &object=objects.back();
          object.name=name.str();
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              return true;
            }
            SPLITTER splitter(line);
            cstr key=splitter.get();
            if(key=="depth"){
              object.depth=splitter.getInt();
            }
            else if(key=="folding"){
              object.folding=splitter.getInt();
            }
            else if(key=="scale"){
              object.scale=splitter.getVector3();
            }
            else if(key=="rotation"){
              object.rotation=splitter.getVector3();
            }
            else if(key=="translation"){
              object.translation=splitter.getVector3();
            }
            else if(key=="visible"){
              object.visible=splitter.getInt();
            }
            else if(key=="locking"){
              object.locking=splitter.getInt();
            }
            else if(key=="shading"){
              object.shading=splitter.getInt();
            }
            else if(key=="facet"){
              object.smoothing=splitter.getFloat();
            }
            else if(key=="color"){
              object.color=splitter.getVector3();
            }
            else if(key=="color_type"){
              object.color_type=splitter.getInt();
            }
            else if(key=="vertex"){
              if(!readObjectVertexChunk(reader, object, splitter.getInt())){
                return false;
              }
            }
            else if(key=="face"){
              if(!readObjectFaceChunk(reader, object, splitter.getInt())){
                return false;
              }
            }
            else if(key=="segment"){
              // ToDo
              continue;
            }
            else if(key=="patch"){
              // ToDo
              continue;
            }
            else if(key=="mirror"){
              object.mirror=splitter.getInt();
            }
            else{
              std::cout << "unknown object key: " << key << std::endl;
            }
          }
          std::cout << "fail to readObjectChunk" << std::endl;
          return false;
        }
      template<class READER> bool 
        readObjectVertexChunk(READER &reader, 
            Object &object, size_t vertex_count)
        {
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              if(object.vertices.size()!=vertex_count){
                std::cout << "invalid vertex count." 
                  << " expected " << vertex_count
                  << ", but " << object.vertices.size()
                  << std::endl;
                return false;
              }
              return true;
            }
            object.vertices.push_back(SPLITTER(line).getVector3());
          }
          std::cout << "fail to readObjectVertexChunk" << std::endl;
          return false;
        }

      template<class READER> bool 
        readObjectFaceChunk(READER &reader,
            Object &object, size_t face_count)
        {
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              if(object.faces.size()!=face_count){
                std::cout << "invalid face count."
                  << " expected " << face_count
                  << ", but " << object.faces.size()
                  << std::endl;
                return false;
              }
              return true;
            }
            if(!readObjectFaceLine(object, line)){
              return false;
            }
          }
          std::cout << "fail to readFaceChunk" << std::endl;
          return false;
        }

      bool 
        readObjectFaceLine(Object &object, cstr line)
        {
          object.faces.push_back(Face());
          Face &face=object.faces.back();
          SPLITTER splitter(line);
          face.index_count=splitter.getInt();
          while(true){
            cstr key=splitter.get();
            if(key==""){
              break;
            }

            if(key=="V"){
              for(size_t i=0; i<face.index_count; ++i){
                face.indices[i]=splitter.getInt();
              }
            }
            else if(key=="M"){
              face.material_index=splitter.getInt();
            }
            else if(key=="UV"){
              for(size_t i=0; i<face.index_count; ++i){
                face.uv[i]=splitter.getVector2();
              }
            }
            else if(key=="COL"){
              for(size_t i=0; i<face.index_count; ++i){
                face.color[i]=
                  fRGBA::createFromUInt(splitter.getInt());
              }
            }
            else{
              std::cout << "unknown face key: " 
                << '"' << key << '"'  << std::endl
                ;
              //return false;
              break;
            }
          }
          return true;
        }

      template<class READER> bool 
        readMaterialChunk(READER &reader, size_t material_count)
        {
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              if(materials.size()!=material_count){
                std::cout << "invalid material count." 
                  << " expected " << material_count
                  << ", but " << materials.size()
                  << std::endl;
                return false;
              }
              return true;
            }
            readMaterialLine(line);
          }
          std::cout << "fail to readMaterialChunk" << std::endl;
          return false;
        }

      void 
        readMaterialLine(cstr line)
        {
          materials.push_back(Material());
          Material &material=materials.back();

          SPLITTER splitter(line);
          material.name=splitter.getQuated().str();
          while(true){
            cstr key=splitter.get();
            if(key==""){
              break;
            }
            else if(key=="shader"){
              material.shader=splitter.getInt();
            }
            else if(key=="col"){
              material.color=splitter.getFloatRGBA();
            }
            else if(key=="dif"){
              material.diffuse=splitter.getFloat();
            }
            else if(key=="amb"){
              material.ambient=splitter.getFloat();
            }
            else if(key=="emi"){
              material.emit=splitter.getFloat();
            }
            else if(key=="spc"){
              material.specular=splitter.getFloat();
            }
            else if(key=="power"){
              material.power=splitter.getFloat();
            }
            else if(key=="tex"){
              material.texture=splitter.getQuated().str();
            }
            else if(key=="aplane"){
              material.alphamap=splitter.getQuated().str();
            }
            else if(key=="bump"){
              material.bumpmap=splitter.getQuated().str();
            }
            else if(key=="vcol"){
              material.vcol=splitter.getInt();
            }
            else{
              std::cout << "unknown material key: \"" << key << '"' << std::endl;
              //assert(false);
              return;
            }
          }
        }

      template<class READER> bool 
        readSceneChunk(READER &reader)
        {
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              return true;
            }
            SPLITTER splitter(line);
            cstr key=splitter.get();
            if(key=="pos"){
              scene.pos=splitter.getVector3();
            }
            else if(key=="lookat"){
              scene.lookat=splitter.getVector3();
            }
            else if(key=="head"){
              scene.head=splitter.getFloat();
            }
            else if(key=="pich") {
              scene.pitch=splitter.getFloat();
            }
            else if(key=="ortho"){
              scene.ortho=splitter.getInt();
            }
            else if(key=="zoom2"){
              scene.zoom2=splitter.getFloat();
            }
            else if(key=="amb"){
              scene.ambient=splitter.getVector3();
            }
            else{
              std::cout << "unknown scene key: " << key << std::endl;
            }
          }
          std::cout << "fail to readSceneChunk" << std::endl;
          return false;
        }

      template<class READER> bool 
        readChunk(READER &reader)
        {
          int level=1;
          while(!reader.isEnd()){
            cstr line=reader.getLine();
            if(line=="}"){
              level--;
              if(level==0){
                return true;
              }
            }
            else if(line.include('{')){
              level+=1;
            }
          }
          return false;
        }

    };


    // IO
    bool IO::read(binary::IReader &input)
    {
      LineReader<IsCRLF, IsWhiteSpace, IsEmpty> 
        reader(input);
      cstr line=reader.getLine();
      if(line!="Metasequoia Document"){
        return false;
      }
      line=reader.getLine();
      if(line!="Format Text Ver 1.0"){
        return false;
      }

      return Implementation(scene, materials, objects).parse(reader);
    }

    bool IO::read(const char *path)
    {
      std::vector<char> all;
      binary::readAll(path, all);
      if(all.empty()){
        return false;
      }
      binary::MemoryReader reader(&all[0], all.size());
      return read(reader);
    }

    bool IO::write(binary::IWriter &writer)
    {
      // header
      writer.printLn("Metasequoia Document");
      writer.printLn("Format Text Ver 1.0");
      writer.printLn("");

      // scene
      writer.printLn("Scene {");
      writer.printLn("\tpos 0.0000 0.0000 1500.0000");
      writer.printLn("\tlookat 0.0000 0.0000 0.0000");
      writer.printLn("\thead -0.5236");
      writer.printLn("\tpich 0.5236");
      writer.printLn("\tortho 0");
      writer.printLn("\tzoom2 5.0000");
      writer.printLn("\tamb 0.250 0.250 0.250");
      writer.printLn("}");

      // materials
      if(materials.size()>0){
        writer.printLn("Material %d {", materials.size());
        /*
        for(size_t i=0; i<materials.size(); ++i){
          Material &m=materials[i];
        }
        */
        writer.printLn("}");
      }

      // objects
      for(size_t i=0; i<objects.size(); ++i){
        Object &o=objects[i];
        writer.printLn("Object \"%s\" {", o.name.c_str());
        writer.printLn("\tdepth 0");
        writer.printLn("\tfolding 0");
        writer.printLn("\tscale 1.000000 1.000000 1.000000");
        writer.printLn("\trotation 0.000000 0.000000 0.000000");
        writer.printLn("\ttranslation 0.000000 0.000000 0.000000");
        writer.printLn("\tvisible 15");
        writer.printLn("\tlocking 0");
        writer.printLn("\tshading 1");
        writer.printLn("\tfacet 59.5");
        writer.printLn("\tcolor 0.898 0.400 0.137");
        writer.printLn("\tcolor_type 0");
        // vertex
        writer.printLn("\tvertex %d {", o.vertices.size());
        for(size_t j=0; j<o.vertices.size(); ++j){
          Vector3 &v=o.vertices[j];
          writer.printLn("\t\t%.4f %.4f %.4f", v.x, v.y, v.z);
        }
        writer.printLn("\t}");
        // face
        writer.printLn("\tface %d {", o.faces.size());
        for(size_t j=0; j<o.faces.size(); ++j){
          Face &f=o.faces[j];

          std::stringstream ss;
          ss.setf(std::ios_base::fixed, std::ios_base::floatfield);
          ss 
            << "\t\t"
            << f.index_count
            ;
          ss << " V(";
          for(size_t k=0; k<f.index_count; ++k){
            if(k){
              ss << ' ';
            }
            ss << f.indices[k];
          }
          ss << ") UV(";
          for(size_t k=0; k<f.index_count; ++k){
            if(k){
              ss << ' ';
            }
            Vector2 &uv=f.uv[k];
            ss 
              << std::setprecision(5) << uv.x 
              << ' ' << std::setprecision(5) << uv.y;
          }
          ss << ")";

          writer.printLn(ss.str().c_str());
        }
        writer.printLn("\t}");
        // close
        writer.printLn("}");
      }
      // Eof
      writer.printLn("Eof");

      return true;
    }

    bool IO::write(const char *path)
    {
      binary::FileWriter writer(path);
      return write(writer);
    }

  }
}
