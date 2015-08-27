#include "vmd.h"
#include "text.h"
#include <algorithm>
#include <string>

namespace meshio {
  namespace vmd {

    template<typename T>
      struct SortKeyFrameList
      {
        typedef T MAP;
        void operator()(typename MAP::value_type &channel)
        {
          channel.second->sort();
        }
      };

    template<class READER>
      void
      readBoneMap(READER &reader, IO &io)
      {
        std::wstring name=
          trim(cp932_to_unicode(reader.getString(15, true)));
        unsigned int frame=reader.getUint();
        IO::BoneMap::iterator found=io.boneMap.find(name);
        if(found==io.boneMap.end()){
          // not found
          found=io.boneMap.insert(
              std::make_pair(name, 
                new KeyFrameList<KeyFrame<BoneKey> >())).first;
          io.boneKeys.push_back(name);
        }
        BoneKey &key=found->second->push(frame).key;

        reader.get(key.pos);
        reader.get(key.q);
        reader.get(key.interpolationX);
        reader.get(key.interpolationY);
        reader.get(key.interpolationZ);
        reader.get(key.interpolationRot);
      }

    template<class READER>
      void
      readMorphMap(READER &reader, IO &io)
      {
        std::wstring name=
          trim(cp932_to_unicode(reader.getString(15, true)));
        unsigned int frame=reader.getUint();
        IO::MorphMap::iterator found=io.morphMap.find(name);
        if(found==io.morphMap.end()){
          // not found
          found=io.morphMap.insert(
              std::make_pair(name, 
                new KeyFrameList<KeyFrame<MorphKey> >())).first;
          io.morphKeys.push_back(name);
        }
        MorphKey &key=found->second->push(frame).key;

        reader.get(key.weight);
      }

    class Implementation
    {
      IO &io_;
      binary::IReader &reader_;

    public:
      Implementation(IO &io, binary::IReader &reader)
        : io_(io), reader_(reader)
      {}

      bool parse()
      {
        // check header
        std::string line=reader_.getString(30, true);
        if(line=="Vocaloid Motion Data file"){
          io_.version="1";
          reader_.get(io_.name);
          return parseBody();
        }
        else if(line=="Vocaloid Motion Data 0002"){
          io_.version="2";
          reader_.get(io_.name);
          return parseBody();
        }
        else{
          //std::cout << "unknown header:" << line << std::endl;
          return false;
        }
      }


    private:
      bool parseBody()
      {
        if(!parseFrame()){
          return false;
        }
        if(!parseMorph()){
          return false;
        }
        if(!parseCamera()){
          return false;
        }
        if(!parseLight()){
          return false;
        }
        // sort
        std::for_each(io_.boneMap.begin(), io_.boneMap.end(), 
            SortKeyFrameList<IO::BoneMap>());
        std::for_each(io_.morphMap.begin(), io_.morphMap.end(), 
            SortKeyFrameList<IO::MorphMap>());
        return true;
      }

      bool parseMorph()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          readMorphMap(reader_, io_);
        }
        return true;
      }

      bool parseFrame()
      {
        unsigned int count=reader_.getUint();
        for(unsigned int i=0; i<count; ++i){
          readBoneMap(reader_, io_);
        }
        return true;
      }

      bool parseCamera()
      {
        return true;
      }

      bool parseLight()
      {
        return true;
      }
    };


    ///////////////////////////////////////////////////////////////////////////////
    //! IO
    ///////////////////////////////////////////////////////////////////////////////
    IO::IO()
    {
    }

    IO::~IO()
    {
      for(BoneMap::iterator it=boneMap.begin(); it!=boneMap.end(); ++it){
        delete it->second;
      }
      boneMap.clear();

      for(MorphMap::iterator it=morphMap.begin(); it!=morphMap.end(); ++it){
        delete it->second;
      }
      morphMap.clear();

    }

    bool IO::read(binary::IReader &reader)
    {
      return Implementation(*this, reader).parse();
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

    bool IO::write(std::ostream &os)
    {
      // not implemented
      return false;
    }

  } // namespace vmd
} // namespace meshio
