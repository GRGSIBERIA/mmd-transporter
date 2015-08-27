/**
 * PMD形式
 * MMDのモデルデータ。バイナリ形式でひとつの頂点が最大２つまでのボーンの
 * ウェイトを保持する単一の頂点配列と頂点インデックス配列をもつ。面は
 * 三角形のみ。
 * また表情モーフィング情報、物理演算向けの剛体情報と拘束情報などをもつ。
 *
 * 座標系
 * 左手 Y-UP
 *
 * 表
 * clock wise ?
 *
 * UV原点
 * left top ?
 *
 * 法線
 * 頂点法線が格納済み。
 *
 * メッシュ
 * 最大頂点数
 * 最大三角形数
 *
 * 裏面の扱い
 * オリジナルではバックカリングをしていないのでやる場合はモデル個別に
 * 対応が必要。
 *
 * 参考サイト
 * http://blog.goo.ne.jp/torisu_tetosuki/e/209ad341d3ece2b1b4df24abf619d6e4
 */

#ifndef MESH_IO_PMD_H_INCLUDED
#define MESH_IO_PMD_H_INCLUDED 

#include "la.h"
#include "text.h"
#include "binary.h"
#include <ostream>
#include <vector>
#include <array>

namespace meshio {
  namespace pmd {

    ////////////////////////////////////////////////////////////
    //! 頂点
    ////////////////////////////////////////////////////////////
    struct Vertex
    {
      //! 座標
      meshio::Vector3 pos;
      //! 法線ベクトル
      meshio::Vector3 normal;
      //! テクスチャUV
      meshio::Vector2 uv;
      //! ブレンディングボーン1
      unsigned short bone0;
      //! ブレンディングボーン2
      unsigned short bone1;
      //! ウェイト[0 - 100]
      unsigned char weight0;
      //! 非エッジ
      unsigned char edge_flag;
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os, const Vertex &rhs)
    {
      os
        << "[Vertex"
        << " pos:" << rhs.pos
        << " normal:" << rhs.normal
        << " uv:" << rhs.uv
        << " bone0:" << rhs.bone0
        << " bone1:" << rhs.bone1
        << " weight0:" << (int)rhs.weight0
        << " edge_flag:" << (int)rhs.edge_flag
        << "]"
        ;
      return os;
    }
#endif

    ////////////////////////////////////////////////////////////
    //! 材質
    ////////////////////////////////////////////////////////////
    struct Material
    {
      //! Diffuse
      meshio::fRGBA diffuse;
      //! Shinness
      float shinness;
      //! Specular
      meshio::fRGB specular;
      //! Ambient
      meshio::fRGB ambient;
      //! トゥーンテクスチャ
      unsigned char toon_index;
      //! 輪郭/影
      unsigned char flag;
      //! 面頂点数
      unsigned int vertex_count;
      //! テクスチャ
      meshio::fixed_string<20> texture;
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os,
        const Material &rhs)
    {
      os
        << "[Material"
        << " diffuse:" << rhs.diffuse
        << " toon_index:" << (int)rhs.toon_index
        << " flag:" << (int)rhs.flag
        << " vertex_count:" << rhs.vertex_count
        << " texture:" << rhs.texture
        << "]"
        ;
      return os;
    }
#endif

    ////////////////////////////////////////////////////////////
    //! ボーン 
    ////////////////////////////////////////////////////////////
    //! ボーンの種類
    enum BONE_TYPE
    {
      // 回転
      BONE_ROTATE=0,
      // 回転と移動
      BONE_ROTATE_MOVE,
      // IK
      BONE_IK,
      // 不明
      BONE_UNKNOWN,
      // IK影響下
      BONE_IK_INFLUENCED,
      // 回転影響下
      BONE_ROTATE_INFLUENCED,
      // IK接続先
      BONE_IK_CONNECT,
      // 非表示
      BONE_INVISIBLE,
      // 捻り
      BONE_TWIST,
      // 回転連動
      BONE_REVOLVE,
    };
    struct Bone
    {
      //! 名前
      meshio::fixed_string<20> name;
      //! 親ボーン
      unsigned short parent_index;
      //! 子ボーン
      unsigned short tail_index;
      //! ボーン種類
      BONE_TYPE type;
      //! 影響IKボーン
      unsigned short ik_index;
      // ボーン座標
      meshio::Vector3 pos;
      //! 英語名
      meshio::fixed_string<20> english_name;
      //! ボーン階層構築用
      Bone* parent;
      meshio::Vector3 tail;
      std::vector<Bone*> children;
      unsigned short index;

      Bone()
        : parent_index(-1), tail_index(-1), type(BONE_UNKNOWN), ik_index(-1), parent(0), index(-1)
      {}
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os,
        const Bone &rhs)
    {
      os
        << "[Bone "
        << '"' << rhs.name << '"'
        << "]"
        ;
      return os;
    }
#endif

    ////////////////////////////////////////////////////////////
    //! IK
    ////////////////////////////////////////////////////////////
    struct IK
    {
      //! IK(IKターゲット)
      unsigned short index;
      //! Target(エフェクター)
      unsigned short target;
      //! エフェクタに連動するボーン数
      unsigned char length;
      //! IK値1。CCD-IK試行回数
      unsigned short iterations;
      //! IK値2。CCD-IK試行一回辺りの影響度
      float weight;
      //! エフェクタに連動するボーン(基本的に親ボーンに遡る)
      std::vector<unsigned short> children;
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os, const IK &rhs)
    {
      os
        << "[IK "
        << "]"
        ;
      return os;
    }
#endif

    ////////////////////////////////////////////////////////////
    //! 表情
    ////////////////////////////////////////////////////////////
    //! 表情の種類
    enum MORPH_TYPE
    {
      //! ベース表情
      MORPH_BASE=0,
      //! まゆ
      MORPH_MAYU,
      //! 目
      MORPH_ME,
      //! リップ
      MORPH_LIP,
      //! その他
      MORPH_OTHER,
    };
    struct Morph
    {
      //! 表情名
      meshio::fixed_string<20> name;
      //! 使用する頂点数
      unsigned int vertex_count;
      //! 分類
      unsigned char type;
      //! 頂点Index
      std::vector<unsigned int> indices;
      //! 移動量
      std::vector<meshio::Vector3> pos_list;
      //! 英語名
      meshio::fixed_string<20> english_name;
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os, const Morph &rhs)
    {
      os
        << "[Morph "
        << '"' << rhs.name << '"'
        << "]"
        ;
      return os;
    }
#endif

    ////////////////////////////////////////////////////////////
    //! ボーン表示枠
    ////////////////////////////////////////////////////////////
    struct BoneGroup
    {
      meshio::fixed_string<50> name;
      meshio::fixed_string<50> english_name;
    };

    ////////////////////////////////////////////////////////////
    //! 剛体
    ////////////////////////////////////////////////////////////
    //! 形状
    enum SHAPE_TYPE
    {
      //! 球
      SHAPE_SPHERE=0,
      //! 箱
      SHAPE_BOX,
      //! カプセル
      SHAPE_CAPSULE,
    };
    //! 剛体タイプ
    enum PROCESS_TYPE
    {
      //! ボーンと同じ動き
      RIGIDBODY_KINEMATICS=0,
      //! 物理演算
      RIGIDBODY_PHYSICS,
      //! 物理演算結果をボーンに反映する
      RIGIDBODY_PHYSICS_WITH_BONE,
    };

    struct RigidBody
    {
      //! 剛体名
      meshio::fixed_string<20> name;
      //! 関連ボーン(ボーン追従とボーン位置合わせで必要)
      unsigned short boneIndex;
      //! グループ
      unsigned char group;
      //! 非衝突グループ
      unsigned short target;
      //! 形状
      SHAPE_TYPE shapeType;
      //! サイズ
      float w;
      float h;
      float d;
      //! 姿勢
      meshio::Vector3 position;
      meshio::Vector3 rotation;
      //! 質量
      float weight;
      //! 物理演算パラメータ(bullet)
      float linearDamping;
      float angularDamping;
      float restitution;
      float friction;
      //! 剛体タイプ
      PROCESS_TYPE processType;
    };

    //! Joint(物理演算でのJointとConstraintは同じ意味)
    struct Constraint
    {
      //! Joint名
      meshio::fixed_string<20> name;
      //! 接続剛体A
      unsigned int rigidA;
      //! 接続剛体B
      unsigned int rigidB;
      //! 位置
      meshio::Vector3 pos;
      //! 回転
      meshio::Vector3 rot;
      //! 移動制限
      meshio::Vector3 constraintPosMin;
      meshio::Vector3 constraintPosMax;
      //! 回転制限
      meshio::Vector3 constraintRotMin;
      meshio::Vector3 constraintRotMax;
      //! ばね
      meshio::Vector3 springPos;
      meshio::Vector3 springRot;
    };


    // IO
    struct IO
    {
      float version;
      meshio::fixed_string<20> name;
      meshio::fixed_string<256> comment;
      std::vector<Vertex> vertices;
      std::vector<unsigned short> indices;
      std::vector<Material> materials;
      std::vector<Bone> bones;
      std::vector<IK> ik_list;
      std::vector<Morph> morph_list;
      std::vector<unsigned short> face_list;
      std::vector<BoneGroup> bone_group_list;
      std::vector<std::pair<unsigned short, unsigned char> > bone_display_list;
      std::array<meshio::fixed_string<100>, 10> toon_textures;
      std::vector<RigidBody> rigidbodies;
      std::vector<Constraint> constraints;

      meshio::fixed_string<20> english_name;
      meshio::fixed_string<256> english_comment;

      IO();
      bool read(const char *path);
      bool write(const char *path);
      bool read(meshio::binary::IReader &reader);
      bool write(meshio::binary::IWriter &writer);
    };
#ifndef SWIG
    inline std::ostream &operator<<(std::ostream &os, const IO &rhs)
    {
      os
        << "<PMD " << rhs.name << std::endl
        << rhs.comment << std::endl
        << "[vertices] " << rhs.vertices.size() << std::endl
        << "[indices] " << rhs.indices.size() << std::endl
        << "[materials] " << rhs.materials.size() << std::endl
        ;
      /*
         std::copy(rhs.materials.begin(), rhs.materials.end(), 
         std::ostream_iterator<Material>(os, ""));

         os
         << "[bones] " << rhs.bones.size() << std::endl
         ;
         std::copy(rhs.bones.begin(), rhs.bones.end(), 
         std::ostream_iterator<Bone>(os, ""));

         os
         << "[ik] " << rhs.ik_list.size() << std::endl
         ;
         std::copy(rhs.ik_list.begin(), rhs.ik_list.end(), 
         std::ostream_iterator<IK>(os, ""));

         os
         << "[morph] " << rhs.morph_list.size() << std::endl
         ;
         std::copy(rhs.morph_list.begin(), rhs.morph_list.end(), 
         std::ostream_iterator<Morph>(os, ""));
       */

      os
        << ">" << std::endl
        ;
      return os;
    }
#endif


  } // namespace pmd
} // namespace meshio

#endif // MESH_IO_PMD_H_INCLUDED
