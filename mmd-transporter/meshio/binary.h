/**
 * バイナリファイルの読み込み補助ライブラリ
 */
#ifndef MESH_IO_BINARY_H_INCLUDED
#define MESH_IO_BINARY_H_INCLUDED

#include "text.h"
#include <fstream>
#include <vector>
#include <assert.h>
#include <stdarg.h>
#include <string.h>

namespace meshio {
  namespace binary {

    static void copyStringAndFillZero(char *dst, const std::string &src)
    {
      size_t i=0;
      for(; i<src.size(); ++i)
      {
        dst[i]=src[i];
        if(src[i]=='\0'){
          break;
        }
      }
      for(; i<src.size(); ++i)
      {
        dst[i]='\0';
      }
    }

    /**
     * データ読み込みインターフェース
     */
    class IReader
    {
    public:
      virtual ~IReader(){}
      virtual unsigned int read(char *buf, unsigned int size)=0;
      virtual unsigned int getPos()const=0;
      virtual bool isEnd()const=0;

      template<typename T>
        bool get(T &t)
        {
          if(read(reinterpret_cast<char*>(&t), sizeof(t))){
            return true;
          }
          else{
            return false;
          }
        }
      template<int LENGTH>
        bool get(fixed_string<LENGTH> &t)
        {
          copyStringAndFillZero(t.begin(), getString(t.size()));
          return true;
        }
      char getChar()
      {
        char byte;
        return get(byte) ? byte : 0;
      }
      std::string getString(unsigned int length, bool isTrim=false)
      {
        std::vector<char> buf(length);
        read(&buf[0], buf.size());

        std::vector<char>::iterator it;
        if(isTrim){
          it=buf.begin();
          for(; it!=buf.end(); ++it){
            if(*it=='\0'){
              break;
            }
          }
        }
        else{
          it=buf.end();
        }
        return std::string(buf.begin(), it);
      }
      unsigned char getUchar()
      {
        unsigned char value;
        return get(value) ? value : 0;
      }
      unsigned short getUshort()
      {
        unsigned short value;
        return get(value) ? value : 0;
      }
      unsigned int getUint()
      {
        unsigned int value;
        return get(value) ? value : 0;
      }
    };

    /**
     * ファイルからの読み込み
     */
    class FileReader : public IReader
    {
      std::ifstream io_;
      unsigned int pos_;
      bool eof_;

    public:
      FileReader(const char *path);
      virtual ~FileReader();
      virtual unsigned int read(char *buf, unsigned int size);
      virtual unsigned int getPos()const;
      virtual bool isEnd()const;
    };

    /**
     * メモリからの読み込み
     */
    class MemoryReader : public IReader
    {
      const char *buf_;
      unsigned int size_;
      unsigned int pos_;

    public:
      MemoryReader(const char *buf, unsigned int size);
      virtual ~MemoryReader();
      virtual unsigned int read(char *buf, unsigned int size);
      virtual unsigned int getPos()const;
      virtual bool isEnd()const;
    };

    void readAll(const char *path, std::vector<char> &all);
#ifdef _WIN32
    void readAll(const wchar_t *path, std::vector<char> &all);
#endif

    /**
     * データ書き込みインターフェース
     */
    class IWriter
    {
    public:
      virtual ~IWriter(){}
      virtual void write(const char *buf, unsigned int size)=0;
      void printLn(const char *fmt, ...)
      {
        char buf[1024];
        va_list list;
        va_start(list, fmt);
        vsprintf(buf, fmt, list);
        write(buf, strlen(buf));
        write("\r\n", 2);
        va_end(list);
      }
      template<int LENGTH>
        void write(const fixed_string<LENGTH> &src)
        {
          write(
              reinterpret_cast<const char*>(src.begin()), 
              src.size());
        }
      template<typename T>
        void writeArray(const T *array, size_t element_count)
        {
          write(
              reinterpret_cast<const char*>(array), 
              sizeof(T)*element_count);
        }
      template<typename T>
        void writeValue(T value)
        {
          writeArray(&value, 1);
        }
    };

    class FileWriter : public IWriter
    {
      FILE *io_;

    public:
      FileWriter(const char *path);
      FileWriter(const wchar_t *path);
      virtual ~FileWriter();
      virtual void write(const char *buf, unsigned int size);
    };

  } // namespace binary
} // namespace meshio

#endif // MESH_IO_BINARY_H_INCLUDED
