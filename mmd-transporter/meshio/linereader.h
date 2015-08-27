#ifndef LINEREADER_H
#define LINEREADER_H

#include "text.h"

namespace meshio 
{
  struct IsCRLF
  {
    bool operator()(char byte)const
    {
      switch(byte)
      {
        case '\n':
        case '\r': // fall through
          return true;

        default:
          return false;
      }
    }
  };

  struct IsWhiteSpace
  {
    bool operator()(char byte)const
    {
      switch(byte)
      {
        case ' ':
        case '\t': // fall through
          return true;

        default:
          return false;
      }
    }
  };

  struct IsEmpty
  {
    bool operator()(cstr line)const
    {
      return line.empty();
    }
  };

  template<class DELIMITER=IsCRLF, 
    class TRIM=IsWhiteSpace,
    class LINESKIP=IsEmpty>
      class LineReader
      {
        binary::IReader &reader_;
        unsigned int lineCount_;
        std::vector<char> buf_;
        bool isEnd_;

      public:
        LineReader(binary::IReader &reader)
          : reader_(reader), lineCount_(0), isEnd_(false)
        {
        }

        cstr getLine()
        {
          while(!isEnd_){
            fill_();
            cstr line;
            if(!buf_.empty()){
              line=trim_();
            }
            if(LINESKIP()(line)){
              continue;
            }
            ++lineCount_;
            return line;
          }
          return cstr();
        }

        unsigned int getLineCount()const
        {
          return lineCount_;
        }

        bool isEnd()const
        {
          return isEnd_;
        }

      private:
        void fill_()
        {
          buf_.clear();
          // skip delimeter
          while(char byte=reader_.getChar()){
            if(DELIMITER()(byte)){
              continue;
            }
            buf_.push_back(byte);
            break;
          }
          while(char byte=reader_.getChar()){
            if(DELIMITER()(byte)){
              break;
            }
            buf_.push_back(byte);
          }
          if(buf_.empty()){
            isEnd_=true;
            return;
          }
        }

        cstr trim_()
        {
          if(buf_.empty()){
            return cstr();
          }

          size_t front=0;
          while(true){
            if(front>=buf_.size()){
              return cstr();
            }
            if(!TRIM()(buf_[front])){
              break;
            }
            ++front;
          }

          size_t back=buf_.size()-1;
          for(; back>=0; --back){
            if(!TRIM()(buf_[back])){
              break;
            }
          }
          assert(front<=back);
          return cstr(&buf_[0]+front, &buf_[0]+back+1);
        }
      };

  template<class DELIMITER=IsWhiteSpace>
    class LineSplitter
    {
      cstr line_;

    public:
      LineSplitter(cstr line)
        : line_(line)
      {
      }

      cstr get()
      {
        const char* head=0;
        const char* tail=0;
        const char *current=line_.begin();
        for(; current!=line_.end();){
          for(; current!=line_.end(); ++current){
            if(!DELIMITER()(*current)){
              head=current;
              break;
            }
          }
          if(head){
            for(; current!=line_.end(); ++current){
              if(DELIMITER()(*current)){
                break;
              }
            }
            tail=current;
          }
          if(tail){
            break;
          }
        }
        if(!tail){
          return cstr();
        }
        line_=cstr(tail+1, line_.end());
        return cstr(head, tail);
      }

      int getInt()
      {
        return atoi(get().begin());
      }

      float getFloat()
      {
        return static_cast<float>(atof(get().begin()));
      }

      Vector2 getVector2()
      {
        float x=getFloat();
        float y=getFloat();
        return Vector2(x, y);
      }

      Vector3 getVector3()
      {
        float x=getFloat();
        float y=getFloat();
        float z=getFloat();
        return Vector3(x, y, z);
      }

      Vector4 getVector4()
      {
        float x=getFloat();
        float y=getFloat();
        float z=getFloat();
        float w=getFloat();
        return Vector4(x, y, z, w);
      }

      fRGBA getFloatRGBA()
      {
        float r=getFloat();
        float g=getFloat();
        float b=getFloat();
        float a=getFloat();
        return fRGBA(r, g, b, a);
      }

      bRGBA getByteRGBA()
      {
        int r=getInt();
        int g=getInt();
        int b=getInt();
        int a=getInt();
        return bRGBA(r, g, b, a);
      }

      cstr getQuated()
      {
        const char *begin=line_.begin();
        for(; begin!=line_.end(); ++begin){
          if(*begin=='"'){
            break;
          }
        }
        begin++;
        assert(begin<=line_.end());

        const char *c=begin+1;
        for(; c!=line_.end(); ++c){
          if(*c=='"'){
            break;
          }
        }

        cstr token=cstr(begin, c);

        // advance
        line_=cstr(c+1, line_.end());

        return token;
      }
    };
}

#endif
