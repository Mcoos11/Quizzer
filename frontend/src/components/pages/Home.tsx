import './Home.css'
import Button from '../Button.tsx'
import InfoImage from '../../../img/info-image_1.jpg'
import HowToImage from '../../../img/how_to_image_1.jpg'
import HowToVideo from '../../../img/how_to_video.mp4'
import Author_1 from '../../../img/author_1.jpg'
import Author_2 from '../../../img/author_2.jpg'
import Author_3 from '../../../img/author_3.jpg'
import Author_4 from '../../../img/author_4.jpg'

import { connect } from 'react-redux';
import { checkAuthenticated } from '../../actions/auth';

function Home({ isAuthenticated }: any) {
    return (
        <>
            <section className="hero">
                <h1>Twórz, rozwiązuj i ucz się z Quizzer</h1>
                <div className="description">Welcome to our platform, the ultimate learning hub for teachers and students. Explore a wide 
range of quizzes and educational resources, and engage with our vibrant community</div>
                <Button className="secondary">Dowiedz się więcej</Button>
            </section>
            <section className="parallax-section-home"></section>

            <section className="about-us">
                <h1>O nas</h1>
                <div>
                    Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
                </div>
            </section>
            
            <section className="info-section">
                <div>
                    <h1>Info</h1>
                    <div>
                        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
                    </div>
                </div>
                <img src={InfoImage}></img>
            </section>
            <section className="slideshow-section">
            </section>

            <section className="how-to-section">
                <div>
                    <h1>Jak używać</h1>
                    <div>
                        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?
                    </div>
                </div>
            </section>
            <div className="video-container">
                <div className="video-outer">
                    <video src={HowToVideo} controls></video>
                </div>
            </div>
            <section className="authors-section">
                <h1>Autorzy</h1>
                <div className="authors-list">
                    <div>
                        <img src={Author_1}></img>
                        Autor 1
                    </div>
                    <div>
                        <img src={Author_2}></img>
                        Autor 2
                    </div>
                    <div>
                        <img src={Author_3}></img>
                        Autor 3
                    </div>
                    <div>
                        <img src={Author_4}></img>
                        Autor 4
                    </div>
                </div>
            </section>
        </>
    )
}
const mapStateToProps = (state: any) => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { checkAuthenticated })(Home);