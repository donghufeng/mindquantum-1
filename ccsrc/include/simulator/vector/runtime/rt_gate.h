//   Copyright 2023 <Huawei Technologies Co., Ltd>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.
#ifndef MQ_SIM_VECTOR_RT_GATE
#define MQ_SIM_VECTOR_RT_GATE
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

#include "core/parameter_resolver.hpp"
#include "ops/basic_gate.hpp"
#include "ops/gate_id.hpp"

namespace mindquantum::sim::rt {
struct Gate {
    GateID gate = GateID::null;
    std::vector<Index> objs;
    std::vector<Index> ctrls;
    double ang = 0;
    Gate() = default;
    Gate(GateID gate, const std::vector<Index> &objs, const std::vector<Index> &ctrls)
        : gate(gate), objs(objs), ctrls(ctrls) {
    }

    void Reset() {
        gate = GateID::null;
        objs = {};
        ctrls = {};
    }
    bool Valid() {
        return gate != GateID::null;
    }
    void AddObj(Index obj) {
        if (std::find(objs.begin(), objs.end(), obj) != objs.end()) {
            throw std::runtime_error("obj qubit " + std::to_string(obj) + " already added.");
        }
        objs.push_back(obj);
    }
    void AddCtrl(Index ctrl) {
        if (std::find(objs.begin(), objs.end(), ctrl) != objs.end()) {
            throw std::runtime_error("ctrl qubit " + std::to_string(ctrl) + " is already in obj qubits.");
        }
        if (std::find(ctrls.begin(), ctrls.end(), ctrl) != ctrls.end()) {
            throw std::runtime_error("ctrl qubit " + std::to_string(ctrl) + " already added.");
        }
        ctrls.push_back(ctrl);
    }
    std::shared_ptr<BasicGate> GetGate_1() {
        switch (gate) {
            case GateID::RX: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RXGate<double>>(pr, objs, ctrls);
            }
            case GateID::RY: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RYGate<double>>(pr, objs, ctrls);
            }
            case GateID::RZ: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RZGate<double>>(pr, objs, ctrls);
            }
            case GateID::PS: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<PSGate<double>>(pr, objs, ctrls);
            }
            case GateID::Rxx: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RxxGate<double>>(pr, objs, ctrls);
            }
            case GateID::Ryy: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RyyGate<double>>(pr, objs, ctrls);
            }
            case GateID::Rzz: {
                auto pr = ParameterResolver<double>();
                pr.SetConst(ang);
                return std::make_shared<RzzGate<double>>(pr, objs, ctrls);
            }
            default:
                throw std::runtime_error(fmt::format("Gate {} not implement.", gate));
        }
    }
    std::shared_ptr<BasicGate> GetGate() {
        switch (gate) {
            case GateID::X:
                return std::make_shared<XGate>(objs, ctrls);
            case GateID::Y:
                return std::make_shared<YGate>(objs, ctrls);
            case GateID::Z:
                return std::make_shared<ZGate>(objs, ctrls);
            case GateID::H:
                return std::make_shared<HGate>(objs, ctrls);
            case GateID::S:
                return std::make_shared<SGate>(objs, ctrls);
            case GateID::T:
                return std::make_shared<TGate>(objs, ctrls);
            case GateID::Sdag:
                return std::make_shared<SdagGate>(objs, ctrls);
            case GateID::Tdag:
                return std::make_shared<TdagGate>(objs, ctrls);
            case GateID::SWAP:
                return std::make_shared<SWAPGate>(objs, ctrls);
            case GateID::ISWAP:
                return std::make_shared<ISWAPGate>(false, objs, ctrls);
            default:
                return GetGate_1();
        }
    }
};
}  // namespace mindquantum::sim::rt
#endif
