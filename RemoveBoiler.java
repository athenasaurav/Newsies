
import java.net.URL;
import de.l3s.boilerpipe.extractors.*;

public class RemoveBoiler {

    public static void main(String[] args) {
        try {
        URL my_url = new URL(args[0]);  

        URL gu_url = new URL("http://www.theguardian.com/commentisfree/2014/oct/05/observer-editorial-housing-problem"); 
        URL bb_url = new URL("http://www.bbc.com/news/world-asia-china-29477731");
        URL us_url = new URL("http://www.usatoday.com/story/opinion/2014/10/02/ebola-dallas-texas-thomas-eric-duncan-liberia-editorials-debates/16615093/");


        URL ws_url = new URL("http://online.wsj.com/articles/matt-kaminski-the-money-feud-spicing-up-the-nationals-orioles-rivalry-1412375893");
        URL uk_url = new URL("http://www.nytimes.com/2014/10/04/opinion/to-give-ukraine-a-chance-sanctions-on-russia-must-continue.html");

        ArticleExtractor a = new ArticleExtractor();
        DefaultExtractor e = new DefaultExtractor();

        String text = e.getText(bb_url);
        System.out.println(text);

        } catch (Exception e) {
            System.out.println("Uh oh");
            System.out.println(e);
            System.exit(1);
        }
    }
}
