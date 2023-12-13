import "./Footer.css";
import LinkedinLogo from "../../Images/LinkedIn Original.svg";
import GithubLogo from "../../Images/Github Original.svg";

const Footer = () => {
  return (
    <div className="footer">
      <ul class="footer__contacts">
        <li className="footer__contact">
          <p className="footer__name">Dillon Arnold</p>
          <div className="footer__links">
            <a
              className="footer__link"
              href="https://www.linkedin.com/in/dillon-arnold-352782275/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={LinkedinLogo}
                alt="LinkedIn logo"
              />
            </a>
            <a
              className="footer__link"
              href="https://github.com/Dillona25"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={GithubLogo}
                alt="GitHub logo"
              />
            </a>
          </div>
        </li>
        <li className="footer__contact">
          <p className="footer__name">Leah DeYoung</p>
          <div className="footer__links">
            <a
              className="footer__link"
              href="https://www.linkedin.com/in/leahdeyoung/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={LinkedinLogo}
                alt="LinkedIn logo"
              />
            </a>
            <a
              className="footer__link"
              href="https://github.com/LDeYoung17"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={GithubLogo}
                alt="GitHub logo"
              />
            </a>
          </div>
        </li>
        <li className="footer__contact">
          <p className="footer__name">Ruven Pinkhasov</p>
          <div className="footer__links">
            <a
              className="footer__link"
              href="https://www.linkedin.com/in/ruven-pinkhasov/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={LinkedinLogo}
                alt="LinkedIn logo"
              />
            </a>
            <a
              className="footer__link"
              href="https://github.com/RPinkha"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                className="footer__icon"
                src={GithubLogo}
                alt="GitHub logo"
              />
            </a>
          </div>
        </li>
      </ul>
      <p className="footer__copyright">
        Copyright 2023 © - All Rights Reserved by The Coding Elves
      </p>
    </div>
  );
};

export default Footer;
