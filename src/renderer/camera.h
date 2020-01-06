#pragma once
#include "render_interface.h"
#include <camera_spec.h>
#include <memory>
#include <optifuser.h>

namespace sapien {
namespace Renderer {
class OptifuserScene;

class OptifuserCamera : public Optifuser::CameraSpec, public ICamera {
public:
  uint32_t mWidth, mHeight;
  std::unique_ptr<Optifuser::OffscreenRenderContext> mRenderContext;
  OptifuserScene *mScene;

public:
  OptifuserCamera(std::string const &name, uint32_t width, uint32_t height, float fovy,
                OptifuserScene *scene, std::string const &shaderDir = "glsl_shader/130");

  // ICamera
  virtual const std::string &getName() const override;
  virtual uint32_t getWidth() const override;
  virtual uint32_t getHeight() const override;
  virtual float getFovy() const override;
  virtual void takePicture() override;
  virtual std::vector<float> getColorRGBA() override;
  virtual std::vector<float> getAlbedoRGBA() override;
  virtual std::vector<float> getNormalRGBA() override;
  virtual std::vector<float> getDepth() override;
  virtual std::vector<int> getSegmentation() override;
  virtual std::vector<int> getObjSegmentation() override;

  virtual IPxrScene *getScene() override;

  // ISensor
  virtual physx::PxTransform getPose() const override;
  virtual void setPose(physx::PxTransform const &pose) override;

#ifdef _USE_OPTIX
  std::vector<float> takeRaytracedPicture(uint32_t samplesPerPixel = 65536,
                                          uint32_t reflectionCount = 4);
#endif

  // Camera intrinsic
  glm::mat4 getCameraMatrix();
};
} // namespace Renderer

} // namespace sapien
