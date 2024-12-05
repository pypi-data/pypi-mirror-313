#pragma once

#include <iterator>
#include <memory>
#include <vector>

#include "common/api.h"

namespace kuzu {
namespace storage {
class MemoryBuffer;
class MemoryManager;
} // namespace storage

namespace common {

struct KUZU_API BufferBlock {
public:
    explicit BufferBlock(std::unique_ptr<storage::MemoryBuffer> block);
    ~BufferBlock();

    uint64_t size() const;
    uint8_t* data() const;

public:
    uint64_t currentOffset;
    std::unique_ptr<storage::MemoryBuffer> block;

    void resetCurrentOffset() { currentOffset = 0; }
};

class InMemOverflowBuffer {

public:
    explicit InMemOverflowBuffer(storage::MemoryManager* memoryManager)
        : memoryManager{memoryManager}, currentBlock{nullptr} {};

    uint8_t* allocateSpace(uint64_t size);

    void merge(InMemOverflowBuffer& other) {
        move(begin(other.blocks), end(other.blocks), back_inserter(blocks));
        // We clear the other InMemOverflowBuffer's block because when it is deconstructed,
        // InMemOverflowBuffer's deconstructed tries to free these pages by calling
        // memoryManager->freeBlock, but it should not because this InMemOverflowBuffer still
        // needs them.
        other.blocks.clear();
        currentBlock = other.currentBlock;
    }

    // Releases all memory accumulated for string overflows so far and re-initializes its state to
    // an empty buffer. If there is a large string that used point to any of these overflow buffers
    // they will error.
    void resetBuffer();

private:
    bool requireNewBlock(uint64_t sizeToAllocate) {
        return currentBlock == nullptr ||
               (currentBlock->currentOffset + sizeToAllocate) > currentBlock->size();
    }

    void allocateNewBlock(uint64_t size);

private:
    std::vector<std::unique_ptr<BufferBlock>> blocks;
    storage::MemoryManager* memoryManager;
    BufferBlock* currentBlock;
};

} // namespace common
} // namespace kuzu
