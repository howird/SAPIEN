#pragma once
#include "sapien/logger.h"
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>
#include <fmt/format.h>

namespace sapien {
namespace logger {

std::shared_ptr<spdlog::logger> getLogger();

template <typename... Args> inline void debug(spdlog::string_view_t fmt, const Args &...args) {
  getLogger()->debug(fmt::runtime(fmt), args...);
};

template <typename... Args> inline void info(spdlog::string_view_t fmt, const Args &...args) {
  getLogger()->info(fmt::runtime(fmt), args...);
};

template <typename... Args> inline void warn(spdlog::string_view_t fmt, const Args &...args) {
  getLogger()->warn(fmt::runtime(fmt), args...);
};

template <typename... Args> inline void error(spdlog::string_view_t fmt, const Args &...args) {
  getLogger()->error(fmt::runtime(fmt), args...);
};

template <typename... Args> inline void critical(spdlog::string_view_t fmt, const Args &...args) {
  getLogger()->critical(fmt::runtime(fmt), args...);
};

}; // namespace logger
} // namespace sapien
