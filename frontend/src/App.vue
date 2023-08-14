<template>
    <div id="wrapper">
        <nav class="navbar is-dark">
            <div class="navbar-brand">
                <router-link to="/" class="navbar-item">
                    <svg class="nav-logo" style="width: 2.0em; height: 2.0em; vertical-align: middle; fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                        <path  d="M50.673152 590.181581l71.227187-33.565491 0 138.349975-71.227187 18.831872L50.673152 590.181617 50.673152 590.181581zM142.367334 734.264115l75.315405-17.19255 0 151.449317-75.315427 0L142.367312 734.264153 142.367334 734.264115zM142.367334 322.482688l75.315405-60.578714L217.682739 459.198423l-75.315405 36.839014L142.367334 322.482669 142.367334 322.482688zM142.367334 546.7904l75.315405-34.379981 0 157.99643-75.315405 19.646464L142.367334 546.790364 142.367334 546.7904zM248.795648 238.164275l103.149466-82.684211 0 239.860926-103.149466 49.93833L248.795648 238.164285 248.795648 238.164275zM50.673152 754.730291l71.227187-15.558349L121.900339 868.520903 50.67318 868.520903 50.67318 754.730277 50.673152 754.730291zM248.795648 710.519398l103.149466-22.919987L351.945114 868.520903 248.795622 868.520903 248.795622 710.519356 248.795648 710.519398zM50.673152 395.341005l71.227187-56.485478 0 166.187997-71.227187 34.379981L50.673152 395.341047 50.673152 395.341005zM248.795648 498.49129l103.149466-48.299008 0 185.834452-103.149466 26.193613L248.795648 498.491335 248.795648 498.49129zM973.326848 238.164275l-27.019469 630.356582-16.373586 0-17.193267-590.244045-311.912755-49.93833-2.459136 179.282227 140.814848 18.831872 2.454016-176.008704 44.207616 7.366758-1.634304 174.36928 134.262374 18.012262 0 53.211922-135.082086-16.372941-1.639424 166.182912 136.72151 9.00608 0 36.019355-137.536102-6.547149-1.639424 176.828314-45.027363 0 2.454016-178.467635-142.449152-6.547149-2.454016 171.095757-44.20766 0L547.613484 681.866782l-169.468621-8.18647 0-49.118698 169.468621 12.279706L547.613484 460.018092l-169.468621-18.831872 0-62.21804 169.468621 22.105498L547.613484 220.152049l-162.921267-26.193613-6.547354-33.565491L973.326848 238.164275zM596.734362 465.74551l-1.639424 173.55479 141.62944 9.820672 2.459136-167.002522L596.734362 465.74551zM596.734362 465.74551"  />
                    </svg>
                </router-link>

                <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu"
                    @click="showMobileMenu = !showMobileMenu">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>

            <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
                <div class="navbar-start">
                    <div class="navbar-item">
                        <form method="get" action="/search">
                            <div class="field has-addons" style="display: none">
                                <div class="search-bar">
                                    <input 
                                        type="text" 
                                        class="input"
                                        placeholder="What are you looking for?" 
                                        name="query" 
                                        style="border-radius: 500px;"
                                    >
                                </div>

                                <button class="button is-success">
                                    <span class="icon">
                                        <i class="fas fa-search"></i>
                                    </span>
                                </button>
                            </div>
                        </form>
                        
                        <form method="get" action="/search">
                            <div class="search">
                                <input
                                    type="text"
                                    class="search__input"
                                    aria-label="search"
                                    placeholder="What are you looking for?"
                                    name="query"
                                />

                                <button class="search__submit" aria-label="submit search">
                                    <span class="icon">
                                        <Icon icon="ic:baseline-search"/>
                                    </span>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="navbar-end">
                    <router-link to="/all-datasets" class="navbar-item" style="display: none;">All Datasets</router-link>
                    <router-link to="/explore" class="navbar-item">Explore Datasets</router-link>
                    <router-link to="/public/publish" class="navbar-item" style="display: none;">Publish
                        Datasets</router-link>
                    <router-link to="/world-map" class="navbar-item" style="display: none;">World Map</router-link>
                    <router-link to="/about" class="navbar-item">About Us</router-link>
                    <router-link to="/taxonomy" class="navbar-item">Taxonomy</router-link>
                    <router-link to="/contact" class="navbar-item">Contact Us</router-link>
                </div>
            </div>
        </nav>

        <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
        </div>
        
        <section class="section">
            <router-view />
        </section>

        <footer class="footer">
            <div class="footer-container">
                <div class="footer-container01">
                    <div class="footer-container02">
                        <div class="columns is-multiline">
                            <div class="column">
                                
                                <div class="column footer-logo-left">
                                    <a href="https://web-en.unipv.it/" target="_blank" rel="noopener noreferrer">
                                        <img src="./assets/images/Unipv_WHITE.svg" alt="University of Pavia" 
                                        style="width: 15.0em;">
                                    </a>
                                    <a href="https://www.eucentre.it/" target="_blank" rel="noopener noreferrer">
                                        <img src="./assets/images/LogoEucentreWhite.svg" alt="Eucentre" 
                                        style="width: 15.0em;">
                                    </a>
                                </div>

                                The Built Environment Test Data website and web services are developed,
                                maintained and hosted by 
                                <strong><a href="https://web-en.unipv.it/" target="_blank" rel="noopener noreferrer" style="color: white">University of Pavia</a></strong>, in collaboration with 
                                <strong><a href="https://www.eucentre.it/" target="_blank" rel="noopener noreferrer" style="color: white">EUCENTRE</a></strong> and 
                                with technical support from the 
                                <strong><a href="https://www.globalquakemodel.org/" target="_blank" rel="noopener noreferrer" style="color: white">GEM Foundation</a></strong>.

                            </div>
                            <div class="column">
                                
                                <div class="column footer-logoright">
                                    <img src="./assets/images/EU-funded-by-logo1.png" alt="Eucentre" 
                                    style="width: 20.0em;">
                                </div>

                                The work presented in this website has received funding from the European Union’s 
                                Horizon Europe research and innovation programme under grant agreement No 101058518. 
                                The European Commission is not responsible for any use that may be made of the information 
                                contained in this website.
                            </div>
                        </div>

                        <div class="footer-nav" style="font-weight: bold">
                            <router-link to="/cookies" class="nav-text">Cookies</router-link>
                            <router-link to="/privacy-terms" class="nav-text">Privacy & Terms</router-link>
                        </div>
                    </div>
                </div>
            </div>

            <div class="icon-container" style="display: none">
                <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
                    <div class="icon-container-1">
                        <svg viewBox="0 0 877.7142857142857 1024" class="media-icons">
                            <path
                                d="M713.143 73.143c90.857 0 164.571 73.714 164.571 164.571v548.571c0 90.857-73.714 164.571-164.571 164.571h-107.429v-340h113.714l17.143-132.571h-130.857v-84.571c0-38.286 10.286-64 65.714-64l69.714-0.571v-118.286c-12-1.714-53.714-5.143-101.714-5.143-101.143 0-170.857 61.714-170.857 174.857v97.714h-114.286v132.571h114.286v340h-304c-90.857 0-164.571-73.714-164.571-164.571v-548.571c0-90.857 73.714-164.571 164.571-164.571h548.571z">
                            </path>
                        </svg>
                    </div>
                </a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
                    <div class="icon-container-1">
                        <svg viewBox="0 0 950.8571428571428 1024" class="media-icons">
                            <path
                                d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z">
                            </path>
                        </svg>
                    </div>
                </a>
                <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
                    <div class="icon-container-1">
                        <svg viewBox="0 0 877.7142857142857 1024" class="media-icons">
                            <path
                                d="M135.429 808h132v-396.571h-132v396.571zM276 289.143c-0.571-38.857-28.571-68.571-73.714-68.571s-74.857 29.714-74.857 68.571c0 37.714 28.571 68.571 73.143 68.571h0.571c46.286 0 74.857-30.857 74.857-68.571zM610.286 808h132v-227.429c0-121.714-65.143-178.286-152-178.286-70.857 0-102.286 39.429-119.429 66.857h1.143v-57.714h-132s1.714 37.143 0 396.571v0h132v-221.714c0-11.429 0.571-23.429 4-32 9.714-23.429 31.429-48 68-48 47.429 0 66.286 36 66.286 89.714v212zM877.714 237.714v548.571c0 90.857-73.714 164.571-164.571 164.571h-548.571c-90.857 0-164.571-73.714-164.571-164.571v-548.571c0-90.857 73.714-164.571 164.571-164.571h548.571c90.857 0 164.571 73.714 164.571 164.571z">
                            </path>
                        </svg>
                    </div>
                </a>
                <a href="https://www.youtube.com" target="_blank" rel="noopener noreferrer">
                    <div class="icon-container-1">
                        <svg viewBox="0 0 1024 1024" class="media-icons">
                            <path
                                d="M406.286 644.571l276.571-142.857-276.571-144.571v287.429zM512 152c215.429 0 358.286 10.286 358.286 10.286 20 2.286 64 2.286 102.857 43.429 0 0 31.429 30.857 40.571 101.714 10.857 82.857 10.286 165.714 10.286 165.714v77.714s0.571 82.857-10.286 165.714c-9.143 70.286-40.571 101.714-40.571 101.714-38.857 40.571-82.857 40.571-102.857 42.857 0 0-142.857 10.857-358.286 10.857v0c-266.286-2.286-348-10.286-348-10.286-22.857-4-74.286-2.857-113.143-43.429 0 0-31.429-31.429-40.571-101.714-10.857-82.857-10.286-165.714-10.286-165.714v-77.714s-0.571-82.857 10.286-165.714c9.143-70.857 40.571-101.714 40.571-101.714 38.857-41.143 82.857-41.143 102.857-43.429 0 0 142.857-10.286 358.286-10.286v0z">
                            </path>
                        </svg>
                    </div>
                </a>
                <a href="https://gitlab.com" target="_blank" rel="noopener noreferrer">
                    <div class="icon-container-1">
                        <svg viewBox="0 0 1024 1024" class="media-icons">
                            <path
                                d="M59.429 403.429l452.571 580-496-360c-13.714-10.286-19.429-28-14.286-44l57.714-176zM323.429 403.429h377.143l-188.571 580zM210.286 53.714l113.143 349.714h-264l113.143-349.714c6.286-17.714 31.429-17.714 37.714 0zM964.571 403.429l57.714 176c5.143 16-0.571 33.714-14.286 44l-496 360 452.571-580zM964.571 403.429h-264l113.143-349.714c6.286-17.714 31.429-17.714 37.714 0z">
                            </path>
                        </svg>
                    </div>
                </a>
            </div>

            <p class="has-text-centered" style="display: none">Copyright © 2023</p>
        </footer>
    </div>
</template>

<script>
import { Icon } from '@iconify/vue'


export default {
    components: {
        Icon,
    },
    data() {
        return {
            showMobileMenu: false,
        }
    },
}
</script>

<style lang="scss">
@import './assets/styles/style.css';
@import './assets/styles/base.scss';
@import '../node_modules/bulma';


.lds-dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
}

.lds-dual-ring:after {
    content: " ";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
}

.footer-logo-left {
    text-align: right;
}

.footer-logo-right {
    text-align: left;
}

@media(max-width: 760px) {
    .footer-logo-left, .footer-logo-right {
        text-align: center;
    }
}

@keyframes lds-dual-ring {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.is-loading-bar {
    height: 0;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;

    &.is-loading {
        height: 80px;
    }
}
</style>
