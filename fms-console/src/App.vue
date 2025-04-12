<template>
  <div id="app">
    <h1>文件管理系统</h1>
    <button @click="openUploadModal">上传文件</button>
    <button @click="openCreateDirModal">创建目录</button>
    <FileTree :nodes="nodes" @delete="handleDelete" @move="handleMove" @copy="handleCopy" />
    <UploadModal v-if="isUploadModalOpen" @close="isUploadModalOpen = false" @upload="handleUpload" />
    <CreateDirModal v-if="isCreateDirModalOpen" @close="isCreateDirModalOpen = false" @create="handleCreateDir" />
    <MoveModal v-if="isMoveModalOpen" :nodes="nodes" @close="isMoveModalOpen = false" @move="handleConfirmMove" :targetNode="moveTargetNode" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import FileTree from './components/FileTree.vue';
import UploadModal from './components/UploadModal.vue';
import CreateDirModal from './components/CreateDirModal.vue';
import MoveModal from './components/MoveModal.vue';

const nodes = ref([]);
const isUploadModalOpen = ref(false);
const isCreateDirModalOpen = ref(false);
const isMoveModalOpen = ref(false);
const moveTargetNode = ref(null);

const fetchNodes = async () => {
  try {
    const response = await axios.get('/api/nodes');
    nodes.value = response.data;
  } catch (error) {
    console.error('获取节点信息失败:', error);
  }
};

const openUploadModal = () => {
  isUploadModalOpen.value = true;
};

const openCreateDirModal = () => {
  isCreateDirModalOpen.value = true;
};

const handleUpload = async (file, parentId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('parentId', parentId);
  try {
    await axios.post('/api/upload', formData);
    await fetchNodes();
    isUploadModalOpen.value = false;
  } catch (error) {
    console.error('文件上传失败:', error);
  }
};

const handleCreateDir = async (name, parentId) => {
  try {
    await axios.post('/api/createDir', { name, parentId });
    await fetchNodes();
    isCreateDirModalOpen.value = false;
  } catch (error) {
    console.error('目录创建失败:', error);
  }
};

const handleDelete = async (id) => {
  try {
    await axios.post('/api/delete', { id });
    await fetchNodes();
  } catch (error) {
    console.error('删除操作失败:', error);
  }
};

const handleMove = (node) => {
  moveTargetNode.value = node;
  isMoveModalOpen.value = true;
};

const handleConfirmMove = async (targetParentId) => {
  try {
    await axios.post('/api/move', { id: moveTargetNode.value.id, parentId: targetParentId });
    await fetchNodes();
    isMoveModalOpen.value = false;
  } catch (error) {
    console.error('移动操作失败:', error);
  }
};

const handleCopy = async (node) => {
  try {
    await axios.post('/api/copy', { id: node.id });
    await fetchNodes();
  } catch (error) {
    console.error('复制操作失败:', error);
  }
};

onMounted(fetchNodes);
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>