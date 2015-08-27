#ifndef MESH_IO_TEXT_H_INCLUDED
#define MESH_IO_TEXT_H_INCLUDED

#ifdef _WINDOWS
#define NOMINMAX
#include <windows.h>
#else
#include <iconv.h>
#endif

#include "la.h"
#include "color.h"
#include <string>
#include <iostream>
#include <vector>
#include <stdlib.h>
#include <cstring>

namespace meshio {

  class cstr
  {
    const char *begin_;
    const char *end_;

  public:
    cstr()
      : begin_(0), end_(0)
    {}

    cstr(const char *begin, const char *end)
      : begin_(begin), end_(end)
    { }

    bool operator==(const char *rhs)const
    {
      const char *l=begin_;
      for(const char *r=rhs; *r; ++r, ++l){
        if(l==end_){
          return false;
        }
        if(*l!=*r){
          return false;
        }
      }
      return l==end_;
    }

    bool operator!=(const char *rhs)const
    {
      return !(*this==rhs);
    }

    bool include(char c)const
    {
      for(const char *l=begin_; l!=end_; ++l){
        if(*l==c){
          return true;
        }
      }
      return false;
    }

    bool startswith(const char *rhs)
    {
      const char *r=rhs;
      for(const char *l=begin_; l!=end_ && *r!='\0'; ++l, ++r){
        if(*l!=*r){
          return false;
        }
      }
      return true;
    }

    bool empty()const
    {
      return begin_==end_;
    }

    std::string str()const{ return std::string(begin_, end_); }
    const char* begin()const{ return begin_; }
    const char* end()const{ return end_; }
    std::pair<const char*, const char*> range()const{ 
      return std::make_pair(begin_, end_); 
    }

    template<typename IsTrim>
      cstr &trim(IsTrim isTrim){
        while(begin_!=end_ && isTrim(*begin_)){
          begin_++;
        }
        while(end_!=begin_ && isTrim(end_[-1])){
          end_--;
        }
        return *this;
      }
  };
#ifndef SWIG
  inline std::ostream &operator<<(std::ostream &os, const cstr &rhs)
  {
    return os << rhs.str();
  }
#endif

  template<int LENGTH>
    class fixed_string
    {
      char begin_[LENGTH];
      char *end_;
    public:
      fixed_string()
        : end_(begin_)
      {
        begin_[0]='\0';;
      }
      fixed_string(const std::string &str)
        : end_(begin_)
      {
        assign(str);
      }
      fixed_string& operator=(const std::string &src)
      {
        assign(src);
        return *this;
      }
      void assign(const std::string &src)
      {
        if(src.empty()){
          return;
        }
        std::string::const_iterator it=src.begin();
        int i;
        for(i=0; 
            i<LENGTH && it!=src.end(); 
            ++i, ++it)
        {
          begin_[i]=*it;
        }
        if(i<LENGTH)
        {
          begin_[i]='\0';
        }
      }
      size_t size()const { return LENGTH; }
      char *begin() { return begin_; }
      const char *begin() const { return begin_; }
      std::string str() const
      {
        const char *end=begin_;
        for(; end!=end_ && *end!='\0'; ++end){
        }
        return std::string(
            static_cast<const char*>(begin_), 
            static_cast<const char*>(end));
      }
    };
#ifndef SWIG
  template<int LENGTH>
    inline std::ostream &operator<<(std::ostream &os, const fixed_string<LENGTH> &rhs)
    {
      return os << rhs.str();
    }
#endif

#if defined(_WINDOWS)
  inline std::wstring to_WideChar(UINT uCodePage, const std::string &text)
  {
    int size=MultiByteToWideChar(uCodePage, 0, text.c_str(), -1, NULL, 0);
    std::vector<wchar_t> buf(size);
    size=MultiByteToWideChar(uCodePage, 0, text.c_str(), -1, &buf[0], buf.size());
    return std::wstring(buf.begin(), buf.begin()+size);
  }

  inline std::string to_MultiByte(UINT uCodePage, const std::wstring &text)
  {
    int size=WideCharToMultiByte(uCodePage, 0, text.c_str(), -1, NULL, 0, 0, NULL);
    std::vector<char> buf(size);
    size=WideCharToMultiByte(uCodePage, 0, text.c_str(), -1, &buf[0], buf.size(), 0, NULL);
    return std::string(buf.begin(), buf.begin()+size);
  }

  inline std::wstring cp932_to_unicode(const std::string &text)
  {
    return to_WideChar(CP_OEMCP, text);
  }

  inline std::string cp932_to_utf8(const std::string &text)
  {
    return to_MultiByte(CP_UTF8, to_WideChar(CP_OEMCP, text));
  }

#else
  inline std::wstring to_unicode(const char *text, const char *fromcode)
  {
    const char* tocode="WCHAR_T";
    iconv_t cd=iconv_open(tocode, fromcode);
    if(cd==(iconv_t)-1){
      std::cerr << "fail to iconv_open: " << fromcode << " --> " << tocode << std::endl;
      return L"";
    }

    // inbuf
    size_t inbytesleft=std::strlen(text);
    char *inbuf=const_cast<char*>(text);
    // outbuf
    std::vector<wchar_t> buf;
    size_t pos=0;
    size_t outbytesleft=0;

    while(inbytesleft){
      buf.resize(buf.size()+inbytesleft);
      wchar_t *woutbuf=&buf[pos];
      outbytesleft=(buf.size()-pos)*sizeof(wchar_t);
      int ret=iconv(cd, &inbuf, &inbytesleft, (char**)&woutbuf, &outbytesleft);
      if(ret==-1){
        std::cerr << "fail to iconv" <<  std::endl;
        return L"";
      }
      pos=woutbuf-&buf[0];
    }
    if(outbytesleft==0){
      buf.push_back('\0');
    }
    iconv_close(cd);

    return &buf[0];
  }

  inline std::wstring cp932_to_unicode(const std::string &text)
  {
    return to_unicode(text.c_str(), "CP932");
  }
#endif

  inline std::wstring trim(const std::wstring &src){
    std::wstring::const_iterator end=src.begin();
    for(; end!=src.end(); ++end){
      if(*end==L'\0'){
        break;
      }
    }
    return std::wstring(src.begin(), end);
  }

} // namespace meshio
#endif // MESH_IO_TEXT_H_INCLUDED
