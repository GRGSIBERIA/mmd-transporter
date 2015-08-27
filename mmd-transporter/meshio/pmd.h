/**
 * PMD�`��
 * MMD�̃��f���f�[�^�B�o�C�i���`���łЂƂ̒��_���ő�Q�܂ł̃{�[����
 * �E�F�C�g��ێ�����P��̒��_�z��ƒ��_�C���f�b�N�X�z������B�ʂ�
 * �O�p�`�̂݁B
 * �܂��\��[�t�B���O���A�������Z�����̍��̏��ƍS�����Ȃǂ����B
 *
 * ���W�n
 * ���� Y-UP
 *
 * �\
 * clock wise ?
 *
 * UV���_
 * left top ?
 *
 * �@��
 * ���_�@�����i�[�ς݁B
 *
 * ���b�V��
 * �ő咸�_��
 * �ő�O�p�`��
 *
 * ���ʂ̈���
 * �I���W�i���ł̓o�b�N�J�����O�����Ă��Ȃ��̂ł��ꍇ�̓��f���ʂ�
 * �Ή����K�v�B
 *
 * �Q�l�T�C�g
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
    //! ���_
    ////////////////////////////////////////////////////////////
    struct Vertex
    {
      //! ���W
      meshio::Vector3 pos;
      //! �@���x�N�g��
      meshio::Vector3 normal;
      //! �e�N�X�`��UV
      meshio::Vector2 uv;
      //! �u�����f�B���O�{�[��1
      unsigned short bone0;
      //! �u�����f�B���O�{�[��2
      unsigned short bone1;
      //! �E�F�C�g[0 - 100]
      unsigned char weight0;
      //! ��G�b�W
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
    //! �ގ�
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
      //! �g�D�[���e�N�X�`��
      unsigned char toon_index;
      //! �֊s/�e
      unsigned char flag;
      //! �ʒ��_��
      unsigned int vertex_count;
      //! �e�N�X�`��
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
    //! �{�[�� 
    ////////////////////////////////////////////////////////////
    //! �{�[���̎��
    enum BONE_TYPE
    {
      // ��]
      BONE_ROTATE=0,
      // ��]�ƈړ�
      BONE_ROTATE_MOVE,
      // IK
      BONE_IK,
      // �s��
      BONE_UNKNOWN,
      // IK�e����
      BONE_IK_INFLUENCED,
      // ��]�e����
      BONE_ROTATE_INFLUENCED,
      // IK�ڑ���
      BONE_IK_CONNECT,
      // ��\��
      BONE_INVISIBLE,
      // �P��
      BONE_TWIST,
      // ��]�A��
      BONE_REVOLVE,
    };
    struct Bone
    {
      //! ���O
      meshio::fixed_string<20> name;
      //! �e�{�[��
      unsigned short parent_index;
      //! �q�{�[��
      unsigned short tail_index;
      //! �{�[�����
      BONE_TYPE type;
      //! �e��IK�{�[��
      unsigned short ik_index;
      // �{�[�����W
      meshio::Vector3 pos;
      //! �p�ꖼ
      meshio::fixed_string<20> english_name;
      //! �{�[���K�w�\�z�p
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
      //! IK(IK�^�[�Q�b�g)
      unsigned short index;
      //! Target(�G�t�F�N�^�[)
      unsigned short target;
      //! �G�t�F�N�^�ɘA������{�[����
      unsigned char length;
      //! IK�l1�BCCD-IK���s��
      unsigned short iterations;
      //! IK�l2�BCCD-IK���s���ӂ�̉e���x
      float weight;
      //! �G�t�F�N�^�ɘA������{�[��(��{�I�ɐe�{�[���ɑk��)
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
    //! �\��
    ////////////////////////////////////////////////////////////
    //! �\��̎��
    enum MORPH_TYPE
    {
      //! �x�[�X�\��
      MORPH_BASE=0,
      //! �܂�
      MORPH_MAYU,
      //! ��
      MORPH_ME,
      //! ���b�v
      MORPH_LIP,
      //! ���̑�
      MORPH_OTHER,
    };
    struct Morph
    {
      //! �\�
      meshio::fixed_string<20> name;
      //! �g�p���钸�_��
      unsigned int vertex_count;
      //! ����
      unsigned char type;
      //! ���_Index
      std::vector<unsigned int> indices;
      //! �ړ���
      std::vector<meshio::Vector3> pos_list;
      //! �p�ꖼ
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
    //! �{�[���\���g
    ////////////////////////////////////////////////////////////
    struct BoneGroup
    {
      meshio::fixed_string<50> name;
      meshio::fixed_string<50> english_name;
    };

    ////////////////////////////////////////////////////////////
    //! ����
    ////////////////////////////////////////////////////////////
    //! �`��
    enum SHAPE_TYPE
    {
      //! ��
      SHAPE_SPHERE=0,
      //! ��
      SHAPE_BOX,
      //! �J�v�Z��
      SHAPE_CAPSULE,
    };
    //! ���̃^�C�v
    enum PROCESS_TYPE
    {
      //! �{�[���Ɠ�������
      RIGIDBODY_KINEMATICS=0,
      //! �������Z
      RIGIDBODY_PHYSICS,
      //! �������Z���ʂ��{�[���ɔ��f����
      RIGIDBODY_PHYSICS_WITH_BONE,
    };

    struct RigidBody
    {
      //! ���̖�
      meshio::fixed_string<20> name;
      //! �֘A�{�[��(�{�[���Ǐ]�ƃ{�[���ʒu���킹�ŕK�v)
      unsigned short boneIndex;
      //! �O���[�v
      unsigned char group;
      //! ��Փ˃O���[�v
      unsigned short target;
      //! �`��
      SHAPE_TYPE shapeType;
      //! �T�C�Y
      float w;
      float h;
      float d;
      //! �p��
      meshio::Vector3 position;
      meshio::Vector3 rotation;
      //! ����
      float weight;
      //! �������Z�p�����[�^(bullet)
      float linearDamping;
      float angularDamping;
      float restitution;
      float friction;
      //! ���̃^�C�v
      PROCESS_TYPE processType;
    };

    //! Joint(�������Z�ł�Joint��Constraint�͓����Ӗ�)
    struct Constraint
    {
      //! Joint��
      meshio::fixed_string<20> name;
      //! �ڑ�����A
      unsigned int rigidA;
      //! �ڑ�����B
      unsigned int rigidB;
      //! �ʒu
      meshio::Vector3 pos;
      //! ��]
      meshio::Vector3 rot;
      //! �ړ�����
      meshio::Vector3 constraintPosMin;
      meshio::Vector3 constraintPosMax;
      //! ��]����
      meshio::Vector3 constraintRotMin;
      meshio::Vector3 constraintRotMax;
      //! �΂�
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
