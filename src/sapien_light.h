#pragma once
#include "renderer/render_interface.h"
#include "sapien_entity.h"

namespace sapien {

class SLight : public SEntity {
public:
  inline physx::PxTransform getPose() const override { return getRendererLight()->getPose(); }
  inline void setPose(physx::PxTransform const &transform) {
    getRendererLight()->setPose(transform);
  }
  inline physx::PxVec3 getColor() const { return getRendererLight()->getColor(); }
  inline void setColor(physx::PxVec3 color) { getRendererLight()->setColor(color); }
  inline bool getShadowEnabled() const { return getRendererLight()->getShadowEnabled(); }
  inline void setShadowEnabled(bool enabled) {
    return getRendererLight()->setShadowEnabled(enabled);
  }

  using SEntity::SEntity;
  virtual Renderer::ILight *getRendererLight() const = 0;

private:
};

class SPointLight : public SLight {
public:
  inline physx::PxVec3 getPosition() const { return getRendererLight()->getPosition(); }
  inline void setPosition(physx::PxVec3 position) { getRendererLight()->setPosition(position); }
  inline void setShadowParameters(float near, float far) {
    getRendererLight()->setShadowParameters(near, far);
  }

  inline SPointLight(SScene *scene, Renderer::IPointLight *light) : SLight(scene), mLight(light) {}

private:
  Renderer::IPointLight *getRendererLight() const override { return mLight; }
  Renderer::IPointLight *mLight;
};

class SDirectionalLight : public SLight {
public:
  inline physx::PxVec3 getDirection() const { return getRendererLight()->getDirection(); }
  inline void setDirection(physx::PxVec3 direction) {
    getRendererLight()->setDirection(direction);
  }
  inline void setShadowParameters(float halfSize, float near, float far) {
    getRendererLight()->setShadowParameters(halfSize, near, far);
  }

  inline SDirectionalLight(SScene *scene, Renderer::IDirectionalLight *light)
      : SLight(scene), mLight(light) {}

private:
  Renderer::IDirectionalLight *getRendererLight() const override { return mLight; }
  Renderer::IDirectionalLight *mLight;
};

class SSpotLight : public SLight {
public:
  inline physx::PxVec3 getPosition() const { return getRendererLight()->getPosition(); }
  inline void setPosition(physx::PxVec3 position) { getRendererLight()->setPosition(position); }
  inline physx::PxVec3 getDirection() const { return getRendererLight()->getDirection(); }
  inline void setDirection(physx::PxVec3 direction) {
    getRendererLight()->setDirection(direction);
  }
  inline void setShadowParameters(float near, float far) {
    getRendererLight()->setShadowParameters(near, far);
  }

  inline SSpotLight(SScene *scene, Renderer::ISpotLight *light) : SLight(scene), mLight(light) {}

private:
  Renderer::ISpotLight *getRendererLight() const override { return mLight; }
  Renderer::ISpotLight *mLight;
};

} // namespace sapien
