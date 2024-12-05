#pragma once

#include "common/vector/value_vector.h"

namespace kuzu {
namespace function {

/**
 * Binary operator assumes function with null returns null. This does NOT applies to binary boolean
 * operations (e.g. AND, OR, XOR).
 */

struct BinaryFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* /*leftValueVector*/, common::ValueVector* /*rightValueVector*/,
        common::ValueVector* /*resultValueVector*/, uint64_t /*resultPos*/, void* /*dataPtr*/) {
        OP::operation(left, right, result);
    }
};

struct BinaryListStructFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* leftValueVector, common::ValueVector* rightValueVector,
        common::ValueVector* resultValueVector, uint64_t /*resultPos*/, void* /*dataPtr*/) {
        OP::operation(left, right, result, *leftValueVector, *rightValueVector, *resultValueVector);
    }
};

struct BinaryMapCreationFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* leftValueVector, common::ValueVector* rightValueVector,
        common::ValueVector* resultValueVector, uint64_t /*resultPos*/, void* dataPtr) {
        OP::operation(left, right, result, *leftValueVector, *rightValueVector, *resultValueVector,
            dataPtr);
    }
};

struct BinaryListExtractFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* leftValueVector, common::ValueVector* rightValueVector,
        common::ValueVector* resultValueVector, uint64_t resultPos, void* /*dataPtr*/) {
        OP::operation(left, right, result, *leftValueVector, *rightValueVector, *resultValueVector,
            resultPos);
    }
};

struct BinaryStringFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* /*leftValueVector*/, common::ValueVector* /*rightValueVector*/,
        common::ValueVector* resultValueVector, uint64_t /*resultPos*/, void* /*dataPtr*/) {
        OP::operation(left, right, result, *resultValueVector);
    }
};

struct BinaryComparisonFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* leftValueVector, common::ValueVector* rightValueVector,
        common::ValueVector* /*resultValueVector*/, uint64_t /*resultPos*/, void* /*dataPtr*/) {
        OP::operation(left, right, result, leftValueVector, rightValueVector);
    }
};

struct BinaryUDFFunctionWrapper {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename OP>
    static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, RESULT_TYPE& result,
        common::ValueVector* /*leftValueVector*/, common::ValueVector* /*rightValueVector*/,
        common::ValueVector* /*resultValueVector*/, uint64_t /*resultPos*/, void* dataPtr) {
        OP::operation(left, right, result, dataPtr);
    }
};

struct BinaryFunctionExecutor {
    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static inline void executeOnValue(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& resultValueVector, uint64_t lPos, uint64_t rPos, uint64_t resPos,
        void* dataPtr) {
        OP_WRAPPER::template operation<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC>(
            ((LEFT_TYPE*)left.getData())[lPos], ((RIGHT_TYPE*)right.getData())[rPos],
            ((RESULT_TYPE*)resultValueVector.getData())[resPos], &left, &right, &resultValueVector,
            resPos, dataPtr);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static void executeBothFlat(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        auto lPos = left.state->getSelVector()[0];
        auto rPos = right.state->getSelVector()[0];
        auto resPos = result.state->getSelVector()[0];
        result.setNull(resPos, left.isNull(lPos) || right.isNull(rPos));
        if (!result.isNull(resPos)) {
            executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                result, lPos, rPos, resPos, dataPtr);
        }
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static void executeFlatUnFlat(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        auto lPos = left.state->getSelVector()[0];
        auto& rightSelVector = right.state->getSelVector();
        if (left.isNull(lPos)) {
            result.setAllNull();
        } else if (right.hasNoNullsGuarantee()) {
            result.setAllNonNull();
            rightSelVector.forEach([&](auto i) {
                executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                    result, lPos, i, i, dataPtr);
            });
        } else {
            rightSelVector.forEach([&](auto i) {
                result.setNull(i, right.isNull(i)); // left is always not null
                if (!result.isNull(i)) {
                    executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left,
                        right, result, lPos, i, i, dataPtr);
                }
            });
        }
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static void executeUnFlatFlat(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        auto rPos = right.state->getSelVector()[0];
        auto& leftSelVector = left.state->getSelVector();
        if (right.isNull(rPos)) {
            result.setAllNull();
        } else if (left.hasNoNullsGuarantee()) {
            result.setAllNonNull();
            leftSelVector.forEach([&](auto i) {
                executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                    result, i, rPos, i, dataPtr);
            });
        } else {
            leftSelVector.forEach([&](auto i) {
                result.setNull(i, left.isNull(i)); // right is always not null
                if (!result.isNull(i)) {
                    executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left,
                        right, result, i, rPos, i, dataPtr);
                }
            });
        }
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static void executeBothUnFlat(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        KU_ASSERT(left.state == right.state);
        auto& resultSelVector = result.state->getSelVector();
        if (left.hasNoNullsGuarantee() && right.hasNoNullsGuarantee()) {
            result.setAllNonNull();
            resultSelVector.forEach([&](auto i) {
                executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                    result, i, i, i, dataPtr);
            });
        } else {
            resultSelVector.forEach([&](auto i) {
                result.setNull(i, left.isNull(i) || right.isNull(i));
                if (!result.isNull(i)) {
                    executeOnValue<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left,
                        right, result, i, i, i, dataPtr);
                }
            });
        }
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC,
        typename OP_WRAPPER>
    static void executeSwitch(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        result.resetAuxiliaryBuffer();
        if (left.state->isFlat() && right.state->isFlat()) {
            executeBothFlat<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                result, dataPtr);
        } else if (left.state->isFlat() && !right.state->isFlat()) {
            executeFlatUnFlat<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                result, dataPtr);
        } else if (!left.state->isFlat() && right.state->isFlat()) {
            executeUnFlatFlat<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                result, dataPtr);
        } else if (!left.state->isFlat() && !right.state->isFlat()) {
            executeBothUnFlat<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, OP_WRAPPER>(left, right,
                result, dataPtr);
        } else {
            KU_ASSERT(false);
        }
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void execute(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryFunctionWrapper>(left, right,
            result, nullptr /* dataPtr */);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeString(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryStringFunctionWrapper>(left,
            right, result, nullptr /* dataPtr */);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeListStruct(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryListStructFunctionWrapper>(
            left, right, result, nullptr /* dataPtr */);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeMapCreation(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryMapCreationFunctionWrapper>(
            left, right, result, dataPtr);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeListExtract(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryListExtractFunctionWrapper>(
            left, right, result, nullptr /* dataPtr */);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeComparison(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryComparisonFunctionWrapper>(
            left, right, result, nullptr /* dataPtr */);
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename RESULT_TYPE, typename FUNC>
    static void executeUDF(common::ValueVector& left, common::ValueVector& right,
        common::ValueVector& result, void* dataPtr) {
        executeSwitch<LEFT_TYPE, RIGHT_TYPE, RESULT_TYPE, FUNC, BinaryUDFFunctionWrapper>(left,
            right, result, dataPtr);
    }

    struct BinarySelectWrapper {
        template<typename LEFT_TYPE, typename RIGHT_TYPE, typename OP>
        static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, uint8_t& result,
            common::ValueVector* /*leftValueVector*/, common::ValueVector* /*rightValueVector*/) {
            OP::operation(left, right, result);
        }
    };

    struct BinaryComparisonSelectWrapper {
        template<typename LEFT_TYPE, typename RIGHT_TYPE, typename OP>
        static inline void operation(LEFT_TYPE& left, RIGHT_TYPE& right, uint8_t& result,
            common::ValueVector* leftValueVector, common::ValueVector* rightValueVector) {
            OP::operation(left, right, result, leftValueVector, rightValueVector);
        }
    };

    template<class LEFT_TYPE, class RIGHT_TYPE, class FUNC, typename SELECT_WRAPPER>
    static void selectOnValue(common::ValueVector& left, common::ValueVector& right, uint64_t lPos,
        uint64_t rPos, uint64_t resPos, uint64_t& numSelectedValues,
        std::span<common::sel_t> selectedPositionsBuffer) {
        uint8_t resultValue = 0;
        SELECT_WRAPPER::template operation<LEFT_TYPE, RIGHT_TYPE, FUNC>(
            ((LEFT_TYPE*)left.getData())[lPos], ((RIGHT_TYPE*)right.getData())[rPos], resultValue,
            &left, &right);
        selectedPositionsBuffer[numSelectedValues] = resPos;
        numSelectedValues += (resultValue == true);
    }

    template<class LEFT_TYPE, class RIGHT_TYPE, class FUNC, typename SELECT_WRAPPER>
    static uint64_t selectBothFlat(common::ValueVector& left, common::ValueVector& right) {
        auto lPos = left.state->getSelVector()[0];
        auto rPos = right.state->getSelVector()[0];
        uint8_t resultValue = 0;
        if (!left.isNull(lPos) && !right.isNull(rPos)) {
            SELECT_WRAPPER::template operation<LEFT_TYPE, RIGHT_TYPE, FUNC>(
                ((LEFT_TYPE*)left.getData())[lPos], ((RIGHT_TYPE*)right.getData())[rPos],
                resultValue, &left, &right);
        }
        return resultValue == true;
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename FUNC, typename SELECT_WRAPPER>
    static bool selectFlatUnFlat(common::ValueVector& left, common::ValueVector& right,
        common::SelectionVector& selVector) {
        auto lPos = left.state->getSelVector()[0];
        uint64_t numSelectedValues = 0;
        auto selectedPositionsBuffer = selVector.getMutableBuffer();
        auto& rightSelVector = right.state->getSelVector();
        if (left.isNull(lPos)) {
            return numSelectedValues;
        } else if (right.hasNoNullsGuarantee()) {
            rightSelVector.forEach([&](auto i) {
                selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, lPos, i, i,
                    numSelectedValues, selectedPositionsBuffer);
            });
        } else {
            rightSelVector.forEach([&](auto i) {
                if (!right.isNull(i)) {
                    selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, lPos, i,
                        i, numSelectedValues, selectedPositionsBuffer);
                }
            });
        }
        selVector.setSelSize(numSelectedValues);
        return numSelectedValues > 0;
    }

    template<typename LEFT_TYPE, typename RIGHT_TYPE, typename FUNC, typename SELECT_WRAPPER>
    static bool selectUnFlatFlat(common::ValueVector& left, common::ValueVector& right,
        common::SelectionVector& selVector) {
        auto rPos = right.state->getSelVector()[0];
        uint64_t numSelectedValues = 0;
        auto selectedPositionsBuffer = selVector.getMutableBuffer();
        auto& leftSelVector = left.state->getSelVector();
        if (right.isNull(rPos)) {
            return numSelectedValues;
        } else if (left.hasNoNullsGuarantee()) {
            leftSelVector.forEach([&](auto i) {
                selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, i, rPos, i,
                    numSelectedValues, selectedPositionsBuffer);
            });
        } else {
            leftSelVector.forEach([&](auto i) {
                if (!left.isNull(i)) {
                    selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, i, rPos,
                        i, numSelectedValues, selectedPositionsBuffer);
                }
            });
        }
        selVector.setSelSize(numSelectedValues);
        return numSelectedValues > 0;
    }

    // Right, left, and result vectors share the same selectedPositions.
    template<class LEFT_TYPE, class RIGHT_TYPE, class FUNC, typename SELECT_WRAPPER>
    static bool selectBothUnFlat(common::ValueVector& left, common::ValueVector& right,
        common::SelectionVector& selVector) {
        uint64_t numSelectedValues = 0;
        auto selectedPositionsBuffer = selVector.getMutableBuffer();
        auto& leftSelVector = left.state->getSelVector();
        if (left.hasNoNullsGuarantee() && right.hasNoNullsGuarantee()) {
            leftSelVector.forEach([&](auto i) {
                selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, i, i, i,
                    numSelectedValues, selectedPositionsBuffer);
            });
        } else {
            leftSelVector.forEach([&](auto i) {
                auto isNull = left.isNull(i) || right.isNull(i);
                if (!isNull) {
                    selectOnValue<LEFT_TYPE, RIGHT_TYPE, FUNC, SELECT_WRAPPER>(left, right, i, i, i,
                        numSelectedValues, selectedPositionsBuffer);
                }
            });
        }
        selVector.setSelSize(numSelectedValues);
        return numSelectedValues > 0;
    }

    // BOOLEAN (AND, OR, XOR)
    template<class LEFT_TYPE, class RIGHT_TYPE, class FUNC>
    static bool select(common::ValueVector& left, common::ValueVector& right,
        common::SelectionVector& selVector) {
        if (left.state->isFlat() && right.state->isFlat()) {
            return selectBothFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinarySelectWrapper>(left, right);
        } else if (left.state->isFlat() && !right.state->isFlat()) {
            return selectFlatUnFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinarySelectWrapper>(left, right,
                selVector);
        } else if (!left.state->isFlat() && right.state->isFlat()) {
            return selectUnFlatFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinarySelectWrapper>(left, right,
                selVector);
        } else {
            return selectBothUnFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinarySelectWrapper>(left, right,
                selVector);
        }
    }

    // COMPARISON (GT, GTE, LT, LTE, EQ, NEQ)
    template<class LEFT_TYPE, class RIGHT_TYPE, class FUNC>
    static bool selectComparison(common::ValueVector& left, common::ValueVector& right,
        common::SelectionVector& selVector) {
        if (left.state->isFlat() && right.state->isFlat()) {
            return selectBothFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinaryComparisonSelectWrapper>(left,
                right);
        } else if (left.state->isFlat() && !right.state->isFlat()) {
            return selectFlatUnFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinaryComparisonSelectWrapper>(
                left, right, selVector);
        } else if (!left.state->isFlat() && right.state->isFlat()) {
            return selectUnFlatFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinaryComparisonSelectWrapper>(
                left, right, selVector);
        } else {
            return selectBothUnFlat<LEFT_TYPE, RIGHT_TYPE, FUNC, BinaryComparisonSelectWrapper>(
                left, right, selVector);
        }
    }
};

} // namespace function
} // namespace kuzu
