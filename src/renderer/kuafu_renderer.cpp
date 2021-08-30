//
// Created by jet on 7/18/21.
//

#include "kuafu_renderer.hpp"
#include "kuafu_scene.hpp"
#include "kuafu_window.hpp"

#include <kuafu.hpp>
#include <spdlog/spdlog.h>


namespace sapien::Renderer {

void KuafuMaterial::setBaseColor(std::array<float, 4> color) {
  mKMaterial->kd = glm::vec3(color[0], color[1], color[2]);
  mKMaterial->d = color[3];
}

void KuafuMaterial::setRoughness(float roughness) {
  mKMaterial->roughness = roughness;
}

void KuafuMaterial::setSpecular(float specular) {
//  mKMaterial->ns = specular;
  spdlog::get("SAPIEN")->warn("specular adjustment not supported");
}

void KuafuMaterial::setMetallic(float metallic) {
  mKMaterial->shininess = metallic;
}

void KuafuMaterial::setTransparent(bool isTransparent, float ior) {
  mKMaterial->illum = isTransparent ? 1 : 2;
  mKMaterial->ior = ior;
}

void KuafuMaterial::setMaterialType(uint32_t type) {
  mKMaterial->illum = type;
}


void KuafuRenderer::setAssetsPath(std::string const &path) {
  mKRenderer.getConfig().setAssetsPath(path);
}

void KuafuRenderer::init() {
  // TODO: kuafu_urgent (window?)
  if (mUseViewer) {
    mKRenderer.setWindow(std::make_shared<KWindow>(
        800, 600, "Viewer", SDL_WINDOW_RESIZABLE, &mKRenderer.getScene()));
    mScene.mUseViewer = mUseViewer;

    auto cam = std::make_shared<KCamera>("view_cam", 800, 600);
    cam->setPosition({-1, 0, 1});
    cam->setFront({1, 0, -1});
    mKRenderer.getScene().setCamera(cam);
  }

  auto& config = mKRenderer.getConfig();
//  spdlog::get("SAPIEN")->warn((size_t)&config);
  config.setGeometryLimit(1000);
  config.setGeometryInstanceLimit(10000);
  config.setTextureLimit(1000);
  config.setAccumulatingFrames(false);
  config.setClearColor(glm::vec4(0, 0, 0, 1));
  config.setPerPixelSampleRate(64);
  mKRenderer.init();
//  mKRenderer.reset();

  mKRenderer.getScene().removeEnvironmentMap();
  mKRenderer.getScene().setGeometries({});
  mKRenderer.getScene().setGeometryInstances({});
}

IPxrScene *KuafuRenderer::createScene(std::string const &name) {
  mScene.pKRenderer = &mKRenderer;
  return &mScene;
};

void KuafuRenderer::removeScene(IPxrScene *scene) {
  spdlog::get("SAPIEN")->warn("removeScene not implemented yet");
};

std::shared_ptr<IPxrMaterial> KuafuRenderer::createMaterial() {
  return std::make_shared<KuafuMaterial>();
};

}