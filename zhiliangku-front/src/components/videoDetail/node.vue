<template>
  <div class="video-node-container">
    <el-scrollbar class="incenter video-node-inner">
      <div v-html="mainData" class="incenter video-node-content"></div>
    </el-scrollbar>
  </div>
</template>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='scss'>
.ideo-node-inner {
    width: 700px;
    height: 440px;
    .el-scrollbar__wrap {
      overflow-y: scroll;
      overflow-x: hidden;
    }
  }
</style>

<style lang='scss' scoped>
  

  .video-node-content {
    width: 700px;
    min-height: 400px;
    // /* background:skyblue; */
  }

  .video-node-container {
    background: #fafafa;
    padding-top: 32px;
  }

</style>
<script>
  import Bus from '../../assets/js/bus'
  export default {
    name: 'notes',
    data() {
      return {
        name: 'notes',
        mainData: '',
      }
    },
    props: {

    },
    created() {
      Bus.$on('noteData', (obj) => {
        this.mainData = (obj + '').replace(/src="/g, 'src="' + this.$myConst.httpUrl);
      })
      if (this.$parent.$parent.noteData) {
        this.mainData = (this.$parent.$parent.noteData + '').replace(/src="/g, 'src="' + this.$myConst.httpUrl);
      }
    }
  }

</script>
