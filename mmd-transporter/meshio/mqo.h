/**
 * MQO形式
 * メタセコイアのモデルデータ。テキスト形式。
 * マテリアル情報と形状データを保持する。
 * モデリング向けに異なる頂点属性を持つ頂点をひとつの頂点として扱っているので、
 * プログラムで頂点配列を作る場合はマテリアル、UVなどが異なる値を持つ頂点を
 * 別の頂点として分離する作業が必要になる。
 * 法線は計算して算出する必要がある。
 *
 * 座標系
 * 右手 Y-UP
 *
 * 面の表
 * clock wise ?
 *
 * UV原点
 * left top ?
 *
 * 法線
 * オブジェクトの保持するスムージング値を参照して面法線から計算する。
 *
 * 裏面の扱い
 * オリジナルではバックカリング有効。
 *
 * MIKOTO方式のボーン
 * MQOは標準でスキニング情報を持たないが、特定のルールでマテリアルとオブジェクト
 * を作成することでこれを作成する。
 *
 * 参考サイト
 * http://www.metaseq.net/metaseq/format.html
 */

#ifndef MESH_IO_MQO_H_INCLUDED
#define MESH_IO_MQO_H_INCLUDED 

#include <iosfwd>
#include <vector>
#include <assert.h>
#include "la.h"
#include "color.h"
#include "text.h"
#include "binary.h"

namespace meshio {
  namespace mqo {

    //! Sceneチャンク
    struct Scene
    {
      meshio::Vector3 pos;
      meshio::Vector3 lookat;
      float head;
      float pitch;
      int ortho;
      float zoom2;
      meshio::Vector3 ambient;
      Scene()
        : head(0), pitch(0), ortho(false), zoom2(2)
      {}
    };
    inline std::ostream &operator<<(std::ostream &os, const Scene &rhs)
    {
      os
        << "<Scene"
        << " pos: " << rhs.pos
        << ", lookat: " << rhs.lookat
        << ", head: " << rhs.head
        << ", pitch: " << rhs.pitch
        << ", ortho: " << rhs.ortho
        << ", zoom2: " << rhs.zoom2
        << ", ambient: " << rhs.ambient
        << ">"
        ;
      return os;
    }

    //! Materialチャンク
    struct Material
    {
      std::string name;
      int shader;
      meshio::fRGBA color;
      float diffuse;
      float ambient;
      float emit;
      float specular;
      float power;
      std::string texture;
      std::string alphamap;
      std::string bumpmap;
      int vcol;

      Material()
        : shader(0), diffuse(1), ambient(0), emit(0), specular(0), power(0),
        vcol(0)
      {}
    };
    inline std::ostream &operator<<(std::ostream &os, const Material &rhs)
    {
      os
        << "<Material "
        << '"' << rhs.name << '"'
        << " shader:" << rhs.shader
        << ", color:" << rhs.color
        << ", diffuse:" << rhs.diffuse
        << ", ambient:" << rhs.ambient
        << ", emit:" << rhs.emit
        << ", specular:" << rhs.specular
        << ", power:" << rhs.power
        << ", texture:\"" << rhs.texture << '"'
        << ", alphamap:\"" << rhs.alphamap << '"'
        << ", bumpmap:\"" << rhs.bumpmap << '"'
        << ">"
        ;
      return os;
    }

    //! faceチャンク
    struct Face
    {
      unsigned int index_count;
      unsigned int indices[4];
      unsigned int material_index;
      meshio::Vector2 uv[4];
      meshio::fRGBA color[4];
      Face()
        : index_count(0), material_index(0)
      {
        indices[0]=0;
        indices[1]=0;
        indices[2]=0;
        indices[3]=0;
        uv[0]=Vector2();
        uv[1]=Vector2();
        uv[2]=Vector2();
        uv[3]=Vector2();
      }
    };
    inline std::ostream &operator<<(std::ostream &os, const Face &rhs)
    {
      switch(rhs.index_count)
      {
        case 2:
          os
            << "<Edge "
            << "indices:{" << rhs.indices[0] << ',' << rhs.indices[1] << "}"
            << ", material_index: " << rhs.material_index
            << ", uv:{" << rhs.uv[0] << ',' << rhs.uv[1] << "}"
            << ", color:{" << rhs.color[0] << ',' << rhs.color[1] << "}"
            << ">"
            ;
          break;

        case 3:
          os
            << "<Triangle "
            << "indices:{" << rhs.indices[0] 
            << ',' << rhs.indices[1] 
            << ',' << rhs.indices[2] << "}"
            << ", material_index: " << rhs.material_index
            << ", uv:{" << rhs.uv[0] << ',' << rhs.uv[1] << ',' << rhs.uv[2] << "}"
            << ", color:{" 
            << rhs.color[0] << ',' << rhs.color[1] << ',' <<  rhs.color[2] << "}"
            << ">"
            ;
          break;

        case 4:
          os
            << "<Rectangle "
            << "indices:{" << rhs.indices[0] 
            << ',' << rhs.indices[1] 
            << ',' << rhs.indices[2] 
            << ',' << rhs.indices[3] << "}"
            << ", material_index: " << rhs.material_index
            << ", uv:{" << rhs.uv[0] << ',' << rhs.uv[1] 
            << ',' <<  rhs.uv[2] << ',' << rhs.uv[3] << "}"
            << ", color:{" << rhs.color[0] 
            << ',' << rhs.color[1] 
            << ',' <<  rhs.color[2] 
            << ',' <<  rhs.color[3] << "}"
            << ">"
            ;
          break;
        default:
          assert(false);
      }

      return os;
    }

    //! Objectチャンク
    struct Object
    {
      std::string name;
      int depth;
      int folding;
      meshio::Vector3 scale;
      meshio::Vector3 rotation;
      meshio::Vector3 translation;
      int visible;
      int locking;
      int shading;
      float smoothing;
      meshio::Vector3 color;
      int color_type;
      int mirror;

      std::vector<meshio::Vector3> vertices;
      std::vector<Face> faces;

      Object()
        : depth(0), folding(0), visible(1), locking(0), shading(0), 
        smoothing(60.0f), color_type(0), mirror(0)
      {}
    };
    inline std::ostream &operator<<(std::ostream &os, const Object &rhs)
    {
      os
        << "<Object "
        << '"' << rhs.name << '"'
        << " vertices:" << rhs.vertices.size()
        << ", faces:" << rhs.faces.size()
        << ">"
        ;
      return os;
    }

    // IO
    struct IO
    {
      Scene scene;
      std::vector<Material> materials;
      std::vector<Object> objects;

      bool read(meshio::binary::IReader &reader);
      bool read(const char *path);
      bool write(meshio::binary::IWriter &writer);
      bool write(const char *path);
    };

  } // namespace mqo
} // namespace meshio

#endif // MESH_IO_MQO_H_INCLUDED
