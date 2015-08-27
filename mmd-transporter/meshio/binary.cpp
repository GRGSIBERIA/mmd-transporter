#include "binary.h"

namespace meshio {
  namespace binary {

    // FileReader
    FileReader::FileReader(const char *path)
      : io_(path, std::ios::binary), pos_(0), eof_(false)
    {
    }

    FileReader::~FileReader()
    {
    }

    unsigned int FileReader::read(char *buf, unsigned int size)
    {
      if(size==0){
        return 0;
      }
      io_.read(buf, size);
      size_t read_size=static_cast<size_t>(io_.gcount());
      if(read_size==0){
        eof_=true;
      }
      pos_+=read_size;
      return read_size;
    }

    unsigned int FileReader::getPos()const
    {
      return pos_;
    }

    bool FileReader::isEnd()const
    {
      return eof_;
    }

    // MemoryReader
    MemoryReader::MemoryReader(const char *buf, unsigned int size)
      : buf_(buf), size_(size), pos_(0)
    {
    }

    MemoryReader::~MemoryReader()
    {
    }

    unsigned int MemoryReader::read(char *buf, unsigned int size)
    {
      if(pos_+size>=size_){
        size=size_-pos_;
      }
      std::copy(&buf_[pos_], &buf_[pos_+size], buf);
      pos_+=size;
      return size;
    }

    unsigned int MemoryReader::getPos()const
    {
      return pos_;
    }

    bool MemoryReader::isEnd()const
    {
      return pos_>=size_;
    }

    // readALL
    static void readALL_(FILE *fp, std::vector<char> &buf)
    {
      int iRet = fseek(fp, 0L, SEEK_END);
      if(iRet!=0){
        return;
      }

      long pos=ftell(fp);
      if(pos == -1){
        return;
      }

      iRet = fseek(fp, 0L, SEEK_SET);
      if(iRet != 0){
        return;
      }

      buf.resize(pos);
      iRet=fread(&buf[0], pos, 1, fp);
    }

    void readAll(const char *path, std::vector<char> &buf)
    {
      FILE* fp = fopen(path, "rb");
      if(fp){
        readALL_(fp, buf);
        fclose(fp);
      }
    }

#ifdef _MSC_VER
    void readAll(const wchar_t *path, std::vector<char> &buf)
    {
      FILE* fp = _wfopen(path, L"rb");
      if(fp){
        readALL_(fp, buf);
        fclose(fp);
      }
    }
#endif

    // FileWriter
    FileWriter::FileWriter(const char *path)
    {
      io_=fopen(path, "wb");
    }

#if _MSC_VER
    FileWriter::FileWriter(const wchar_t *path)
    {
      io_=_wfopen(path, L"wb");
    }
#endif

    FileWriter::~FileWriter()
    {
      fclose(io_);
    }

    void FileWriter::write(const char *buf, unsigned int size)
    {
      fwrite(buf, size, 1, io_);
    }


  } // namespace binary
} // namespace meshio
