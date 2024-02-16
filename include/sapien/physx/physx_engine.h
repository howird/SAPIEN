#pragma once
#include <PxPhysicsAPI.h>
#include <map>
#include <memory>

namespace sapien {
namespace physx {
class PhysxEngine {
public:
  static std::shared_ptr<PhysxEngine> Get(float toleranceLength = 0.1f,
                                          float toleranceSpeed = 0.2f);

  static std::shared_ptr<PhysxEngine> GetIfExists();

  PhysxEngine(float toleranceLength, float toleranceSpeed);
  ::physx::PxPhysics *getPxPhysics() const { return mPxPhysics; }

  // ::physx::PxCudaContextManager *getCudaContextManager() const { return mCudaContextManager; };
  ::physx::PxCudaContextManager *getCudaContextManager(int cudaId);// const { return mCudaContextManager; };

  ~PhysxEngine();

private:
  ::physx::PxPhysics *mPxPhysics;
  ::physx::PxFoundation *mPxFoundation;

  std::map<int, ::physx::PxCudaContextManager *> mCudaContextManagers; // per device context

  // ::physx::PxCudaContextManager *mCudaContextManager{nullptr};
};

} // namespace physx
} // namespace sapien
