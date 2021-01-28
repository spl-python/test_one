<template>
    <div class="block">
        <el-carousel  height="720px" :interval="3000" arrow="always">
            <el-carousel-item v-for="(banner, key) in banner_list" :key="key">
                <a :href="banner.link"><img :src="banner.img" alt="" class="pic"></a>

            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
export default {
    name: "Banner",
    data() {
        return {
            banner_list: []
        }
    },
    methods: {
        get_banner() {
            this.$axios({
                url: this.$settings.HOST + 'api/banner/',
                method: 'get'
            }).then(res => {
                console.log(res)
                this.banner_list = res.data
            }).catch(error => {
                console.log(error);
            })
        }
    },
    created() {
        this.get_banner()
    }
}
</script>

<style scoped>
.el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
}
/*.pic{*/
/*    height: 400px;*/
/*    width: 534px;*/
/*    margin-left: 440px;*/
/*    margin-top: 150px;*/
/*}*/
.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}
</style>
