#include "pmd.h"
#include "text.h"
#ifndef _WIN32
#include "win32.h"
#endif
#include <iostream>


namespace meshio {
  namespace pmd {

    // IO
    bool IO::write(const char *path)
    {
      binary::FileWriter w(path);
      return write(w);
    }

    // 38bytes
    template<class READER>
      void
      read(READER &reader, Vertex &v)
      {
        unsigned int pos=reader.getPos();
        reader.get(v.pos);
        reader.get(v.normal);
        reader.get(v.uv);
        reader.get(v.bone0);
        reader.get(v.bone1);
        reader.get(v.weight0);
        reader.get(v.edge_flag);
        assert(reader.getPos()-pos==38);
      }

    // 70bytes
    template<class READER>
      void
      read(READER &reader, Material &m)
      {
        unsigned int pos=reader.getPos();
        reader.get(m.diffuse);
        reader.get(m.shinness);
        reader.get(m.specular);
        reader.get(m.ambient);
        reader.get(m.toon_index);
        reader.get(m.flag);
        reader.get(m.vertex_count);
        reader.get(m.texture);
        assert(reader.getPos()-pos==70);
      }

    // 39bytes
    template<class READER>
      void
      read(READER &reader, Bone &b)
      {
        unsigned int pos=reader.getPos();
        reader.get(b.name);
        reader.get(b.parent_index);
        reader.get(b.tail_index);
        b.type=static_cast<BONE_TYPE>(reader.getUchar());
        reader.get(b.ik_index);
        reader.get(b.pos);
        assert(reader.getPos()-pos==39);
      }

    // 11+2xIK_COUNT bytes
    template<class READER>
      void
      read(READER &reader, IK &ik)
      {
        // 11bytes
        reader.get(ik.index);
        reader.get(ik.target);
        reader.get(ik.length);
        reader.get(ik.iterations);
        reader.get(ik.weight);
        // 2 x length bytes
        for(unsigned short j=0; j<ik.length; ++j){
          ik.children.push_back(reader.getUshort());
        }
      }

    // 25+12xMORPH_COUNT bytes
    template<class READER>
      void
      read(READER &reader, Morph &m)
      {
        // 25bytes
        reader.get(m.name);
        reader.get(m.vertex_count);
        m.type=static_cast<MORPH_TYPE>(reader.getUchar());
        // 12 x vertex_count bytes
        for(unsigned short i=0; i<m.vertex_count; ++i){
          m.indices.push_back(reader.getUint());
          m.pos_list.push_back(Vector3());
          reader.get(m.pos_list.back());
        }
      }

    // 83bytes
    template<class READER>
      void
      read(READER &reader, RigidBody &r)
      {
        unsigned int pos=reader.getPos();
        reader.get(r.name);
        reader.get(r.boneIndex);
        reader.get(r.group);
        reader.get(r.target);
        r.shapeType=static_cast<SHAPE_TYPE>(reader.getUchar());
        reader.get(r.w);
        reader.get(r.h);
        reader.get(r.d);
        reader.get(r.position);
        reader.get(r.rotation);
        reader.get(r.weight);
        reader.get(r.linearDamping);
        reader.get(r.angularDamping);
        reader.get(r.restitution);
        reader.template get<float>(r.friction);
        r.processType=static_cast<PROCESS_TYPE>(reader.getUchar());
        assert(reader.getPos()-pos==83);
      }

    // 124bytes
    template<class READER>
      void
      read(READER &reader, Constraint &c)
      {
        unsigned int base_pos=reader.getPos();
        reader.get(c.name);
        reader.get(c.rigidA);
        reader.get(c.rigidB);
        reader.get(c.pos);
        reader.get(c.rot);
        reader.get(c.constraintPosMin);
        reader.get(c.constraintPosMax);
        reader.get(c.constraintRotMin);
        reader.get(c.constraintRotMax);
        reader.get(c.springPos);
        reader.get(c.springRot);
        assert(reader.getPos()-base_pos==124);
      }

    class Impl
    {
      IO &io_;
      binary::IReader &reader_;

    public:
      Impl(IO &io, binary::IReader &reader)
        : io_(io), reader_(reader)
      {}

      bool parse()
      {
        if(!parseHeader()){
          return false;
        }
        if(!parseVertices()){
          return false;
        }
        if(!parseIndices()){
          return false;
        }
        if(!parseMaterials()){
          return false;
        }
        if(!parseBones()){
          return false;
        }
        if(!parseIK()){
          return false;
        }
        if(!parseMorph()){
          return false;
        }
        if(!parseFaceList()){
          return false;
        }
        if(!parseBoneGroupList()){
          return false;
        }
        if(!parseBoneList()){
          return false;
        }
        if(reader_.isEnd()){
          return true;
        }

        ////////////////////////////////////////////////////////////
        // extended data
        ////////////////////////////////////////////////////////////
        // english
        ////////////////////////////////////////////////////////////
        if(reader_.getChar()){
          if(!parseEnglishName()){
            return false;
          }
          if(!parseEnglishBone()){
            return false;
          }
          if(!parseEnglishMorph()){
            return false;
          }
          if(!parseEnglishBoneList()){
            return false;
          }
        }
        if(reader_.isEnd()){
          return true;
        }

        // toone texture
        ////////////////////////////////////////////////////////////
        if(!parseToonTextures()){
          return false;
        }
        if(reader_.isEnd()){
          return true;
        }

        // physics
        ////////////////////////////////////////////////////////////
        if(!parseRigid()){
          return false;
        }
        if(!parseConstraint()){
          return false;
        }

        // end
        assert(reader_.isEnd());

        return true;
      }

    private:
      bool parseConstraint()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          io_.constraints.push_back(Constraint());
          read(reader_, io_.constraints.back());
        }
        return true;
      }

      bool parseRigid()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          io_.rigidbodies.push_back(RigidBody());
          read(reader_, io_.rigidbodies.back());
        }
        return true;
      }

      bool parseToonTextures()
      {
        for(size_t i=0; i<10; ++i){
          reader_.get(io_.toon_textures[i]);
        }
        return true;
      }

      bool parseEnglishBoneList()
      {
        for(size_t i=0; i<io_.bone_group_list.size(); ++i){
            reader_.get(io_.bone_group_list[i].english_name);
        }
        return true;
      }

      bool parseEnglishMorph()
      {
        int count=io_.morph_list.size()-1;
        for(int i=0; i<count; ++i){
          reader_.get(io_.morph_list[i].english_name);
        }
        return true;
      }

      bool parseEnglishBone()
      {
        for(size_t i=0; i<io_.bones.size(); ++i){
          reader_.get(io_.bones[i].english_name);
        }
        return true;
      }

      bool parseEnglishName()
      {
        reader_.get(io_.english_name);
        reader_.get(io_.english_comment);
        return true;
      }

      bool parseBoneList()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          unsigned short bone=reader_.getUshort();
          unsigned char disp=reader_.getUchar();
          io_.bone_display_list.push_back(std::make_pair(bone, disp));
        }
        return true;
      }

      bool parseBoneGroupList()
      {
        unsigned int count=reader_.getUchar();
        for(unsigned int i=0; i<count; ++i){
          io_.bone_group_list.push_back(BoneGroup());
          reader_.get(io_.bone_group_list.back().name);
        }
        return true;
      }

      bool parseFaceList()
      {
        unsigned int count=reader_.getUchar();
        for(unsigned int i=0; i<count; ++i){
          io_.face_list.push_back(reader_.getUshort());
        }
        return true;
      }

      bool parseMorph()
      {
        unsigned int count=reader_.getUshort();
        for(unsigned int i=0; i<count; ++i){
          io_.morph_list.push_back(Morph());
          read(reader_, io_.morph_list.back());
        }
        return true;
      }

      bool parseIK()
      {
        unsigned int count=reader_.getUshort();
        for(unsigned int i=0; i<count; ++i){
          io_.ik_list.push_back(IK());
          read(reader_, io_.ik_list.back());
        }
        return true;
      }

      bool parseBones()
      {
        unsigned int count=reader_.getUshort();
        for(unsigned int i=0; i<count; ++i){
          io_.bones.push_back(Bone());
          read(reader_, io_.bones.back());
        }
        return true;
      }

      bool parseMaterials()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          io_.materials.push_back(Material());
          read(reader_, io_.materials.back());
        }
        return true;
      }

      bool parseIndices()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          io_.indices.push_back(reader_.getUshort());
        }
        return true;
      }

      bool parseVertices()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          io_.vertices.push_back(Vertex());
          read(reader_, io_.vertices.back());
        }
        return true;
      }

      bool parseHeader()
      {
        if(reader_.getString(3)!="Pmd"){
          //std::cout << "invalid pmd" << std::endl;
          return false;
        }
        reader_.get(io_.version);
        if(io_.version!=1.0){
          std::cout << "invalid vesion: " << io_.version <<std::endl;
          return false;
        }
        reader_.get(io_.name);
        reader_.get(io_.comment);
        return true;
      }

    };

    // IO
    IO::IO()
      : version(0)
    {
      for(int i=0; i<10; ++i){
        char toon[100];
        sprintf(toon, "toon%02d.bmp", i+1);
        toon_textures[i]=fixed_string<100>(std::string(toon));;
      }
    }

    bool IO::read(binary::IReader &input)
    {
      Impl impl(*this, input);
      if(!impl.parse()){
        return false;
      }

      ////////////////////////////////////////////////////////////
      // post process
      ////////////////////////////////////////////////////////////
      if(!morph_list.empty()){
        // validate morph
        assert(morph_list[0].type==MORPH_BASE);
        // check base
        Morph &base=morph_list[0];
        for(size_t i=0; i<base.vertex_count; ++i){
          assert(vertices[base.indices[i]].pos==base.pos_list[i]);
        }
        // check each face
        for(size_t i=1; i<morph_list.size(); ++i){
          Morph &m=morph_list[i];
          assert(m.type!=MORPH_BASE);
        }
      }
      ////////////////////////////////////////////////////////////
      // setup bone
      ////////////////////////////////////////////////////////////
      for(size_t i=0; i<bones.size(); ++i){
        Bone &bone=bones[i];
        bone.index=i;
        if(bone.parent_index!=0xFFFF){
          bone.parent=&bones[bone.parent_index];
          bone.parent->children.push_back(&bone);
        }
        if(bone.tail_index==0){
          bone.tail=Vector3(0, 0, 0);
        }
        else{
          bone.tail=bones[bone.tail_index].pos;
        }
      }

      return true;
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

    bool IO::write(binary::IWriter &w)
    {
      w.write("Pmd", 3);
      w.writeValue<float>(version);
      w.write(name);
      w.write(comment);

      // vertices
      //std::cout << "vertices" << std::endl;
      w.writeValue<DWORD>(vertices.size());
      for(size_t i=0; i<vertices.size(); ++i){
        Vertex &v=vertices[i];
        w.writeValue<float>(v.pos.x);
        w.writeValue<float>(v.pos.y);
        w.writeValue<float>(v.pos.z);
        w.writeValue<float>(v.normal.x);
        w.writeValue<float>(v.normal.y);
        w.writeValue<float>(v.normal.z);
        w.writeValue<float>(v.uv.x);
        w.writeValue<float>(v.uv.y);
        w.writeValue<WORD>(v.bone0);
        w.writeValue<WORD>(v.bone1);
        w.writeValue<BYTE>(v.weight0);
        w.writeValue<BYTE>(v.edge_flag);
      }

      // faces
      //std::cout << "faces" << std::endl;
      w.writeValue<DWORD>(indices.size());
      if(indices.size()>0){
        w.writeArray<WORD>(&indices[0], indices.size());
      }

      // materials
      //std::cout << "materials" << std::endl;
      w.writeValue<DWORD>(materials.size());
      for(size_t i=0; i<materials.size(); ++i){
        Material &m=materials[i];
        w.writeValue<float>(m.diffuse.r);
        w.writeValue<float>(m.diffuse.g);
        w.writeValue<float>(m.diffuse.b);
        w.writeValue<float>(m.diffuse.a);
        w.writeValue<float>(m.shinness);
        w.writeValue<float>(m.specular.r);
        w.writeValue<float>(m.specular.g);
        w.writeValue<float>(m.specular.b);
        w.writeValue<float>(m.ambient.r);
        w.writeValue<float>(m.ambient.g);
        w.writeValue<float>(m.ambient.b);
        w.writeValue<BYTE>(m.toon_index);
        w.writeValue<BYTE>(m.flag);
        w.writeValue<DWORD>(m.vertex_count);
        w.write(m.texture);
      }

      // bones
      //std::cout << "bones" << std::endl;
      w.writeValue<WORD>(bones.size());
      for(size_t i=0; i<bones.size(); ++i){
        Bone &b=bones[i];
        w.write(b.name);
        w.writeValue<WORD>(b.parent_index);
        w.writeValue<WORD>(b.tail_index);
        w.writeValue<BYTE>(b.type);
        w.writeValue<WORD>(b.ik_index);
        w.writeValue<float>(b.pos.x);
        w.writeValue<float>(b.pos.y);
        w.writeValue<float>(b.pos.z);
      }

      // ik
      //std::cout << "ik" << std::endl;
      w.writeValue<WORD>(ik_list.size());
      for(size_t i=0; i<ik_list.size(); ++i){
        IK &ik=ik_list[i];
        w.writeValue<WORD>(ik.index);
        w.writeValue<WORD>(ik.target);
        w.writeValue<BYTE>(ik.length);
        w.writeValue<WORD>(ik.iterations);
        w.writeValue<float>(ik.weight);
        WORD parent_index=bones[ik.target].parent_index;
        for(size_t j=0; j<ik.length; 
            ++j, parent_index=bones[parent_index].parent_index){
          w.writeValue<WORD>(parent_index);
        }
      }

      // morph
      //std::cout << "morph" << std::endl;
      w.writeValue<WORD>(morph_list.size());
      for(size_t i=0; i<morph_list.size(); ++i){
        Morph &m=morph_list[i];
        w.write(m.name);
        w.writeValue<DWORD>(m.indices.size());
        w.writeValue<BYTE>(m.type);
        for(size_t j=0; j<m.indices.size(); ++j){
          w.writeValue<DWORD>(m.indices[j]);
          Vector3 &pos=m.pos_list[j];
          w.writeValue<float>(pos.x);
          w.writeValue<float>(pos.y);
          w.writeValue<float>(pos.z);
        }
      }

      // face list
      //std::cout << "face list" << std::endl;
      w.writeValue<BYTE>(face_list.size());
      if(face_list.size()>0){
        w.writeArray<WORD>(&face_list[0], face_list.size());
      }

      // bone name list
      //std::cout << "bone name list" << std::endl;
      w.writeValue<BYTE>(bone_group_list.size());
      for(size_t i=0; i<bone_group_list.size(); ++i){
        // 50bytes
        w.write(bone_group_list[i].name);
      }

      // bone list
      //std::cout << "bone list" << std::endl;
      w.writeValue<DWORD>(bone_display_list.size());
      for(size_t i=0; i<bone_display_list.size(); ++i){
        w.writeValue<WORD>(bone_display_list[i].first);
        w.writeValue<BYTE>(bone_display_list[i].second);
      }

      ////////////////////////////////////////////////////////////
      // extend
      ////////////////////////////////////////////////////////////
      w.writeValue<char>(0x01);

      ////////////////////////////////////////////////////////////
      // english names
      ////////////////////////////////////////////////////////////
      w.write(english_name);
      w.write(english_comment);

      for(size_t i=0; i<bones.size(); ++i){
        w.write(bones[i].english_name);
      }

      // skip base
      for(size_t i=1; i<morph_list.size(); ++i){
        w.write(morph_list[i].english_name);
      }

      for(size_t i=0; i<bone_group_list.size(); ++i){
        w.write(bone_group_list[i].english_name);
      }

      ////////////////////////////////////////////////////////////
      // toon textures
      ////////////////////////////////////////////////////////////
      for(size_t i=0; i<10; ++i){
        w.write(toon_textures[i]);
      }

      ////////////////////////////////////////////////////////////
      // rigid bodies
      ////////////////////////////////////////////////////////////
      w.writeValue<DWORD>(rigidbodies.size());
      for(size_t i=0; i<rigidbodies.size(); ++i){
        RigidBody &rb=rigidbodies[i];
        w.write(rb.name);
        w.writeValue<WORD>(rb.boneIndex);
        w.writeValue<BYTE>(rb.group);
        w.writeValue<WORD>(rb.target);
        w.writeValue<BYTE>(rb.shapeType);
        w.writeValue<float>(rb.w);
        w.writeValue<float>(rb.h);
        w.writeValue<float>(rb.d);
        w.writeValue<float>(rb.position.x);
        w.writeValue<float>(rb.position.y);
        w.writeValue<float>(rb.position.z);
        w.writeValue<float>(rb.rotation.x);
        w.writeValue<float>(rb.rotation.y);
        w.writeValue<float>(rb.rotation.z);
        w.writeValue<float>(rb.weight);
        w.writeValue<float>(rb.linearDamping);
        w.writeValue<float>(rb.angularDamping);
        w.writeValue<float>(rb.restitution);
        w.writeValue<float>(rb.friction);
        w.writeValue<BYTE>(rb.processType);
      }

      ////////////////////////////////////////////////////////////
      // constraints
      ////////////////////////////////////////////////////////////
      w.writeValue<DWORD>(constraints.size());
      for(size_t i=0; i<constraints.size(); ++i){
        Constraint &c=constraints[i];
        w.write(c.name);
        w.writeValue<DWORD>(c.rigidA);
        w.writeValue<DWORD>(c.rigidB);
        w.writeValue<float>(c.pos.x);
        w.writeValue<float>(c.pos.y);
        w.writeValue<float>(c.pos.z);
        w.writeValue<float>(c.rot.x);
        w.writeValue<float>(c.rot.y);
        w.writeValue<float>(c.rot.z);
        w.writeValue<float>(c.constraintPosMin.x);
        w.writeValue<float>(c.constraintPosMin.y);
        w.writeValue<float>(c.constraintPosMin.z);
        w.writeValue<float>(c.constraintPosMax.x);
        w.writeValue<float>(c.constraintPosMax.y);
        w.writeValue<float>(c.constraintPosMax.z);
        w.writeValue<float>(c.constraintRotMin.x);
        w.writeValue<float>(c.constraintRotMin.y);
        w.writeValue<float>(c.constraintRotMin.z);
        w.writeValue<float>(c.constraintRotMax.x);
        w.writeValue<float>(c.constraintRotMax.y);
        w.writeValue<float>(c.constraintRotMax.z);
        w.writeValue<float>(c.springPos.x);
        w.writeValue<float>(c.springPos.y);
        w.writeValue<float>(c.springPos.z);
        w.writeValue<float>(c.springRot.x);
        w.writeValue<float>(c.springRot.y);
        w.writeValue<float>(c.springRot.z);
      }

      return true;
    }


  } // namespace pmd
} // namespace meshio

