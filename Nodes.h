#pragma once

#include <string>
#include "RTTI.h"

struct BaseNode : public IRttiTypeIdProvider {
    virtual ~BaseNode() = default;

    bool bypass = false;
};

struct SourceNode : public BaseNode {
    RTTI_HAS_TYPE_ID

    std::string inputFilePath;
};

struct DestinationNode : public BaseNode {
    RTTI_HAS_TYPE_ID

    bool includeDebugInfo = false;
    std::string outputFilePath;
};

struct MultiplierNode : public BaseNode {
    RTTI_HAS_TYPE_ID

    double multiplier;
};

struct InverterNode : public BaseNode {
    RTTI_HAS_TYPE_ID
};
