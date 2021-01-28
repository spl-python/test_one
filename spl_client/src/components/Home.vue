<template>
    <div>
        <Header></Header>
        <Banner></Banner>
        <Footer></Footer>
        <CartItme></CartItme>
    </div>
</template>

<script>
import Header from "./common/Header";
import Footer from "./common/Footer";
import Banner from "./Banner";
import CartItme from "./CartItem";

export default {
    name: "Home",
    components: {
        Header: Header,
        Footer: Footer,
        Banner: Banner,
    }
}
</script>

<style scoped>

</style>
