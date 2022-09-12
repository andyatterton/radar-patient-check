<a name="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/renalreg/radar-patient-check">
    <img src="images/UKKA Kidney Blue.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Radar Patient Check</h3>

  <p align="center">
    An API for checking that a patient identifier is present in <a href="https://ukkidney.org/rare-renal/homepage"><strong>Radar</strong></a>
    <br />
    <a href="https://github.com/renalreg/radar-patient-check/issues">Report Bug</a>
    ·
    <a href="https://github.com/renalreg/radar-patient-check/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## About The Project

This API was created to allow other applications to verify if a patient is present in <a href="https://ukkidney.org/rare-renal/homepage"><strong>Radar</strong></a> using memberships found in the <a href="https://ukkidney.org/audit-research/data-permissions/ukrdc"><strong>UKRDC</strong></a> database.

### Built With

[![Python][python.org]][python-url] [![Fastapi][fastapi.tiangolo.com]][fastapi-url]

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

<a href="https://www.python.org/downloads/">Install python</a>

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/renalreg/radar-patient-check.git
   ```
2. Create a virtual enviroment
   ```sh
   python -m venv venv
   ```
3. Activate enviroment<br>
   CMD
   ```cmd
   venv/scripts/activate
   ```
   Bash
   ```sh
   source venv/bin/activate
   ```
4. Install requirements packages
   ```sh
   python -m pip install -r requirements.txt
   ```
5. Create a .env file with the following variables and populate

   ```python
   SQLALCHEMY_DATABASE_URL = ""
   APIKEYS = ["", ""]

   # For testing. Exclude for production
   FAKEKEY = ""
   FAKEIDENTIFIER = ""
   ```

6. Start the server. Only use reload for development

   ```python
   uvicorn radar_patient_check.main:app --reload
   ```

   <br />

<!-- LICENSE -->

## License

Distributed under the APGL License. See `LICENSE` for more information.
<br />
<br />

<!-- CONTACT -->

## Contact

Renal Registry - [@RenalRadar](https://twitter.com/@RenalRadar) - rrsystems@renalregistry.nhs.uk

Project Link: [https://github.com/renalreg/radar-patient-check](https://github.com/renalreg/radar-patient-check)

<br />

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [UKRDC-SQLA](https://github.com/renalreg/ukrdc-sqla)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/renalreg/radar-patient-check.svg?style=for-the-badge
[contributors-url]: https://github.com/renalreg/radar-patient-check/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/renalreg/radar-patient-check.svg?style=for-the-badge
[forks-url]: https://github.com/renalreg/radar-patient-check/network/members
[stars-shield]: https://img.shields.io/github/stars/renalreg/radar-patient-check.svg?style=for-the-badge
[stars-url]: https://github.com/renalreg/radar-patient-check/stargazers
[issues-shield]: https://img.shields.io/github/issues/renalreg/radar-patient-check.svg?style=for-the-badge
[issues-url]: https://github.com/renalreg/radar-patient-check/issues
[license-shield]: https://img.shields.io/github/license/renalreg/radar-patient-check.svg?style=for-the-badge
[license-url]: https://github.com/renalreg/radar-patient-check/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/company/ukkidney/
[product-screenshot]: images/screenshot.png
[next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[next-url]: https://nextjs.org/
[react.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[react-url]: https://reactjs.org/
[vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[vue-url]: https://vuejs.org/
[angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[angular-url]: https://angular.io/
[svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[svelte-url]: https://svelte.dev/
[laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[laravel-url]: https://laravel.com
[bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[bootstrap-url]: https://getbootstrap.com
[jquery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[jquery-url]: https://jquery.com
[python.org]: https://img.shields.io/badge/python-ffd03f?style=for-the-badge&logo=python&logoColor=#3776AB
[python-url]: https://www.python.org/
[fastapi.tiangolo.com]: https://img.shields.io/badge/fastapi-ffffff?style=for-the-badge&logo=fastapi&logoColor=05998b
[fastapi-url]: https://fastapi.tiangolo.com/
[sqlmodel.tiangolo.com]: https://img.shields.io/badge/sqlmodel-ffffff?style=for-the-badge&logo=sqlmodel&logoColor=7e56c2
[sqlmodel-url]: https://sqlmodel.tiangolo.com/
