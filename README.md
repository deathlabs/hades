<table>
  <tr>
    <td rowspan="3" align="center" valign="middle">
      <img src="hades.svg" width="250" height="250" alt="HADES Logo" />
    </td>
    <td>
      <h2><code>HADES</code></h2>
      Harnessing AI to Disrupt and Evaluate Security (HADES)
      <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#getting-started">Getting Started</a></li>
        <li><a href="docs/architecture/README.md">Architecture</a></li>
        <li><a href="docs/contributing/README.md">Contributing</a></li>
        <li><a href="LICENSE">License</a></li>
        <li><a href="#credit">Credit</a></li>
      </ul>
    </td>
  </tr>
</table>

## Introduction
HADES is a a cyber adversary emulation app built to promote decentralized cyber defense training. It's for when cyber defenders need a red team to practice against, but the time, money, or people they have available doesn't support their training needs. 

Have you ever been told you have to wait for annual training exercise to test your mettle against a realistic threat? What about funding? Do you need a dirt cheap option for developing your blue team skills where your tools are? Then, HADES is for you! 

HADES was built by a cyber defender who is tired of being on "blue team bench warmer" and eager to defend the network.

## Getting Started
Follow the steps below if you want to run HADES (these instructions assume you already have `git`, `make`, and `docker` installed as well as a valid OpenAI API key). For more information, please [read the docs](docs/README.md).

**Step 1.** Clone this repository and then, change directories to it.
```bash
git clone https://github.com/deathlabs/hades
cd hades
```

**Step 2.** Create a file called `.env.local.secrets` and add the content below to it. Ensure the value used for `OPENAI_API_KEY` is an actual OpenAI API key.
```bash
RABBITMQ_USERNAME=hades
RABBITMQ_PASSWORD=hades
OPENAI_API_KEY=sk-...
``` 

**Step 3.** Build all the containers that makeup `hades` using the provided `Makefile`.  
```bash
make
```

**Step 4.** Start `hades` using the command below using the provided `Makefile`.
```bash
make start
```

## Credit
* [Collin Siebener](https://collinsiebener.com) is the artist who created the HADES logo
* Various icons used in HADES' architecture diagram were borrowed from [Freepik](https://www.freepik.com/)
