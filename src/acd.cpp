#include "sapien/acd.h"
#include "sapien/sapien_shape.h"
#include <coacd.h>

namespace sapien {

std::vector<std::shared_ptr<SConvexMeshGeometry>>
CoACD(std::shared_ptr<SNonconvexMeshGeometry> g) {
  coacd::Mesh mesh;
  for (uint32_t i = 0; i < g->vertices.size() / 3; ++i) {
    mesh.vertices.push_back({g->vertices[3 * i], g->vertices[3 * i + 1], g->vertices[3 * i + 2]});
  }
  for (uint32_t i = 0; i < g->indices.size() / 3; ++i) {
    mesh.indices.push_back({g->indices[3 * i], g->indices[3 * i + 1], g->indices[3 * i + 2]});
  }
  auto meshes = CoACD(mesh);

  std::vector<std::shared_ptr<SConvexMeshGeometry>> result;
  for (auto &m : meshes) {
    auto newMesh = std::make_shared<SConvexMeshGeometry>();
    newMesh->scale = g->scale;
    newMesh->rotation = g->rotation;
    for (auto &v : m.vertices) {
      newMesh->vertices.push_back(v[0]);
      newMesh->vertices.push_back(v[1]);
      newMesh->vertices.push_back(v[2]);
    }
    for (auto &i : m.indices) {
      newMesh->indices.push_back(i[0]);
      newMesh->indices.push_back(i[1]);
      newMesh->indices.push_back(i[2]);
    }
    result.push_back(newMesh);
  }
  return result;
}

} // namespace sapien
