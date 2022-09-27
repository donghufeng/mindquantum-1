//   Copyright 2022 <Huawei Technologies Co., Ltd>
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

#ifndef TERMS_OPERATOR_BASE_EXTERNAL_OPS_HPP
#define TERMS_OPERATOR_BASE_EXTERNAL_OPS_HPP

#include <type_traits>
#include <utility>

#include "config/common_type.hpp"
#include "config/details/binary_operators_helpers.hpp"
#include "config/type_traits.hpp"

#include "experimental/core/config.hpp"
#include "experimental/core/traits.hpp"
#include "experimental/ops/gates/terms_operator_base.hpp"
#include "experimental/ops/gates/traits.hpp"

#if MQ_HAS_CONCEPTS
#    include "config/concepts.hpp"

#    include "experimental/core/concepts.hpp"
#endif  // MQ_HAS_CONCEPTS

// =============================================================================

namespace mindquantum::ops {
namespace details {

template <typename type_t>
struct my_trait {
    using type = typename std::remove_cvref_t<type_t>::coefficient_t;

    template <typename other_t>
    using new_type_t = typename std::remove_cvref_t<type_t>::template new_derived_t<other_t>;
};
}  // namespace details

// -----------------------------------------------------------------------------+

#if MQ_HAS_CONCEPTS
#    define MQ_DEFINE_BINOP_COMMUTATIVE(op, op_impl)                                                                   \
        MQ_DEFINE_BINOP_TERM_OPS_SCALAR_LEFT_(op, op_impl, concepts::not_terms_op, concepts::terms_op)                 \
        MQ_DEFINE_BINOP_TERM_OPS_SCALAR_RIGHT_(op, op_impl, concepts::terms_op, concepts::not_terms_op)                \
        MQ_DEFINE_BINOP_TERM_OPS_TERMS_(op, op_impl, concepts::terms_op, concepts::terms_op)
#    define MQ_DEFINE_BINOP_NON_COMMUTATIVE(op, op_impl, op_inv)                                                       \
        MQ_DEFINE_BINOP_TERM_OPS_TERMS_(op, op_impl, concepts::terms_op, concepts::terms_op)                           \
        MQ_DEFINE_BINOP_TERM_OPS_SCALAR_RIGHT_(op, op_impl, concepts::terms_op, concepts::not_terms_op)                \
        template <concepts::not_terms_op scalar_t, concepts::terms_op rhs_t>                                           \
        auto operator op(scalar_t&& lhs, rhs_t&& rhs) {                                                                \
            return (op_inv);                                                                                           \
        }
#    define MQ_DEFINE_BINOP_SCALAR_RIGHT_ONLY(op, op_impl)                                                             \
        MQ_DEFINE_BINOP_TERM_OPS_SCALAR_RIGHT_(op, op_impl, concepts::terms_op, concepts::not_terms_op)

#else
template <typename lhs_t, typename rhs_t, typename = void>
struct lhs_and_scalar : std::false_type {};
template <typename lhs_t, typename rhs_t>
struct lhs_and_scalar<lhs_t, rhs_t,
                      std::enable_if_t<traits::is_terms_operator_v<lhs_t> && !traits::is_terms_operator_v<rhs_t>>>
    : std::true_type {};

template <typename lhs_t, typename rhs_t, typename = void>
struct scalar_and_rhs : std::false_type {};
template <typename lhs_t, typename rhs_t>
struct scalar_and_rhs<lhs_t, rhs_t,
                      std::enable_if_t<!traits::is_terms_operator_v<lhs_t> && traits::is_terms_operator_v<rhs_t>>>
    : std::true_type {};

#    define MQ_DEFINE_BINOP_COMMUTATIVE(op, op_impl)                                                                   \
        template <typename lhs_t, typename rhs_t,                                                                      \
                  typename                                                                                             \
                  = std::enable_if_t<(traits::is_terms_operator_v<lhs_t> && traits::is_terms_operator_v<rhs_t>)        \
                                     || lhs_and_scalar<lhs_t, rhs_t>::value || scalar_and_rhs<lhs_t, rhs_t>::value>>   \
        auto operator op(lhs_t&& lhs, rhs_t&& rhs) {                                                                   \
            MQ_BINOP_COMPLETE_IMPL_(                                                                                   \
                (MQ_BINOP_IMPL_(arithmetic_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, lhs, rhs)),              \
                (MQ_BINOP_IMPL_(arithmetic_scalar_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, lhs, rhs)),       \
                (MQ_BINOP_IMPL_(arithmetic_scalar_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, rhs, lhs)),       \
                traits::is_terms_operator_v<lhs_t>, traits::is_terms_operator_v<rhs_t>)                                \
        }
#    define MQ_DEFINE_BINOP_NON_COMMUTATIVE(op, op_impl, op_inv)                                                       \
        template <typename lhs_t, typename rhs_t,                                                                      \
                  typename                                                                                             \
                  = std::enable_if_t<(traits::is_terms_operator_v<lhs_t> && traits::is_terms_operator_v<rhs_t>)        \
                                     || lhs_and_scalar<lhs_t, rhs_t>::value || scalar_and_rhs<lhs_t, rhs_t>::value>>   \
        auto operator op(lhs_t&& lhs, rhs_t&& rhs) {                                                                   \
            MQ_BINOP_COMPLETE_IMPL_(                                                                                   \
                (MQ_BINOP_IMPL_(arithmetic_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, lhs, rhs)),              \
                (MQ_BINOP_IMPL_(arithmetic_scalar_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, lhs, rhs)),       \
                (op_inv), traits::is_terms_operator_v<lhs_t>, traits::is_terms_operator_v<rhs_t>)                      \
        }
#    define MQ_DEFINE_BINOP_SCALAR_RIGHT_ONLY(op, op_impl)                                                             \
        template <typename lhs_t, typename rhs_t, typename = std::enable_if_t<lhs_and_scalar<lhs_t, rhs_t>::value>>    \
        auto operator op(lhs_t&& lhs, rhs_t&& rhs) {                                                                   \
            return MQ_BINOP_IMPL_(arithmetic_scalar_op_impl, op_impl MQ_BINOP_COMMA details::my_trait, lhs, rhs);      \
        }
#endif  // MQ_HAS_CONCEPTS

MQ_DEFINE_BINOP_COMMUTATIVE(+, config::details::plus_equal)
MQ_DEFINE_BINOP_COMMUTATIVE(*, config::details::multiplies_equal)
MQ_DEFINE_BINOP_NON_COMMUTATIVE(-, config::details::minus_equal, (-rhs + lhs))
MQ_DEFINE_BINOP_SCALAR_RIGHT_ONLY(/, config::details::divides_equal)

#undef MQ_BINOP_COMMA
#undef MQ_DEFINE_BINOP_COMMUTATIVE
#undef MQ_DEFINE_BINOP_NON_COMMUTATIVE
#undef MQ_DEFINE_BINOP_SCALAR_RIGHT_ONLY
#undef MQ_BINOP_IMPL_

// =============================================================================

#if MQ_HAS_CONCEPTS
template <concepts::terms_op lhs_t, concepts::terms_op rhs_t>
#else
template <typename lhs_t, typename rhs_t,
          typename = std::enable_if_t<(traits::is_terms_operator_v<lhs_t> && traits::is_terms_operator_v<rhs_t>)>>
#endif  // MQ_HAS_CONCEPTS
auto operator==(const lhs_t& lhs, const rhs_t& rhs) {
    return lhs.is_equal(rhs);
}

#if !MQ_HAS_OPERATOR_NOT_EQUAL_SYNTHESIS
#    if MQ_HAS_CONCEPTS
template <concepts::terms_op lhs_t, concepts::terms_op rhs_t>
#    else
template <typename lhs_t, typename rhs_t,
          typename = std::enable_if_t<(traits::is_terms_operator_v<lhs_t> && traits::is_terms_operator_v<rhs_t>)>>
#    endif  // MQ_HAS_CONCEPTS
auto operator!=(const lhs_t& lhs, const rhs_t& rhs) {
    return !lhs.is_equal(rhs);
}
#endif  // !MQ_HAS_OPERATOR_NOT_EQUAL_SYNTHESIS
}  // namespace mindquantum::ops

#endif /* TERMS_OPERATOR_BASE_EXTERNAL_OPS_HPP */
