# AI-AGENT : CLI AI Assistant

A simple command-line interface that sends prompts to Google's Gemini API and
prints the response directly to your terminal.

### Features

- Accepts a natural language prompt as a positional argument
- Authenticates with the Gemini API via a `GEMINI_API_KEY` environment variable
- Supports a `--verbose` flag for detailed token usage output

### Usage

Basic usage:

```sh
uv run main.py "What is the meaning of life?"

example using verbose

uv run main.py "What is the meaning of life?" --verbose

User prompt: What is the meaning of life?
Prompt tokens: 8
Response tokens: 674
That's one of humanity's most profound and enduring questions, and famously, there's no single, universally agreed-upon answer. The "meaning of life" is largely a philosophical, spiritual, and deeply personal inquiry.

Here are some common perspectives on what the meaning of life might be:

1.  **No Inherited Meaning (Existentialism):** Many philosophers, particularly existentialists, argue that life has no inherent, pre-ordained meaning. Instead, we are condemned to be free to *create* our own meaning through our choices, actions, and values. It's not found, but forged.
    *   *Key idea:* You are responsible for defining your own purpose.

2.  **Divine Purpose (Religious/Spiritual):** For billions worldwide, the meaning of life is provided by a higher power or spiritual framework. This often involves:
    *   **Serving God/Deity:** Fulfilling a divine plan, adhering to moral codes, and worshipping.
    *   **Spiritual Growth:** Achieving enlightenment, reaching a higher state of consciousness, or preparing for an afterlife.
    *   *Key idea:* Meaning is given to us by a greater force or cosmic design.

3.  **Human Flourishing (Humanism/Eudaimonism):** This perspective suggests that the meaning of life lies in achieving our full potential as human beings, living a good and virtuous life, contributing to the well-being of others, and finding happiness and fulfillment.
    *   *Key idea:* Meaning is found in maximizing human potential, well-being, and positive impact.

4.  **Connection and Love:** Many people find life's greatest meaning in their relationships with others – family, friends, romantic partners, and community. Love, empathy, compassion, and shared experiences provide deep purpose and joy.
    *   *Key idea:* Meaning is derived from our bonds and interactions with others.

5.  **Contribution and Legacy:** For some, meaning comes from making a positive difference in the world, leaving behind something of value, or contributing to something larger than themselves, whether it's through work, art, activism, or raising children.
    *   *Key idea:* Meaning is in our impact on the world and future generations.

6.  **Experience and Appreciation:** This view emphasizes the value of simply experiencing life in all its forms – joy, sorrow, beauty, wonder, learning, adventure. The meaning is in the journey itself, embracing every moment.
    *   *Key idea:* Meaning is in the richness and depth of our lived experiences.

7.  **The Biological Imperative:** From a purely biological standpoint, the "meaning" of life could be seen as survival and reproduction – passing on our genes. However, this often feels insufficient to satisfy the human quest for existential meaning.

**In summary:**

The "meaning of life" isn't a fixed destination, but often a **personal journey of discovery and creation.** It's about what you choose to value, what inspires you, what gives you purpose, and how you choose to live your life. It can evolve over time, and it's something each individual must grapple with and define for themselves.
(ai_agent) adrian_coding@PROCODING:~/workspace/ai_agent$ 