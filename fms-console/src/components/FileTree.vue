<template>
  <ul>
    <li v-for="node in filteredNodes" :key="node.id">
      <span @click="toggleExpand(node)">{{ node.name }}</span>
      <span v-if="node.type === 'file'"> (文件) </span>
      <span v-if="node.type === 'folder'"> (文件夹) </span>
      <button @click="handleDelete(node.id)">删除</button>
      <button @click="handleMove(node)">移动</button>
      <button @click="handleCopy(node)">复制</button>
      <FileTree v-if="node.expanded" :nodes="getChildNodes(node.id)" @delete="handleDelete" @move="handleMove" @copy="handleCopy" />
    </li>
  </ul>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  }
});

const emits = defineEmits(['delete', 'move', 'copy']);

const toggleExpand = (node) => {
  node.expanded = !node.expanded;
};

const getChildNodes = (parentId) => {
  return props.nodes.filter(node => node.parent_node_id === parentId && !node.is_deleted);
};

const filteredNodes = props.nodes.filter(node => node.parent_node_id === null && !node.is_deleted);

const handleDelete = (id) => {
  emits('delete', id);
};

const handleMove = (node) => {
  emits('move', node);
};

const handleCopy = (node) => {
  emits('copy', node);
};
</script>

<style scoped>
ul {
  list-style-type: none;
}
</style>