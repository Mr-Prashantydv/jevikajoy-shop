# Paper Boat hero — 24 October 2026

Status: local development theme, not published to the live store. The owner rejected visible product displays and gave creative freedom to generate a new direction. This supersedes the earlier merchandise-led concept for this iteration; it does not change character canon.

## Direction

The five original friends sail a giant yellow paper boat through sunlit clouds. Character connection and imaginative play lead the image. Editable copy identifies the shop: “Character tees for ages 4–12”, “Wear a little wonder.” and “Shop character tees”. No product displays, price claims or promotional discounts appear in the artwork.

## Assets and provenance

Generated with the built-in image generation tool, not the CLI. Original outputs copied without pixel edits:

- `assets/jjw-hero-paper-boat-desktop.png` — 1672 × 941; original `C:/Users/krish/.codex/generated_images/01a16ce0-396f-7010-ad67-f9e94e181d2b/exec-90bc8efd-d26c-46a9-882c-95f9bd669679.png`.
- `assets/jjw-hero-paper-boat-mobile.png` — 941 × 1672; original `C:/Users/krish/.codex/generated_images/01a16ce0-396f-7010-ad67-f9e94e181d2b/exec-a0ac1364-4c55-4e91-a9c5-2dfa65450ea0.png`.

Desktop references: all five character turnaround sheets under `C:/Users/krish/Downloads/character/characters/`: `Jevika's Turnaround.png`, `ChatGPT Image Sep 29, 2026, 12_17_07 AM.png` (Joy), `Brutus Turnaround.png`, `Minku's Turnaround.png`, `ChatGPT Image Sep 29, 2026, 12_22_04 AM.png` (Pinki). Mobile references: generated desktop plus the same Jevika, Joy, Minku and Pinki sheets; Brutus identity comes from the desktop scene.

## Implementation

Only `sections/hero.liquid` consumes the new art. Native framing with separate responsive sources keeps the full cast visible. Text is real HTML supplied by section settings, one h1, with the shared brand button and locale-aware collection URL. Both merchant image pickers remain available. The header has extra artwork clearance at tablet widths. Mobile copy overlays the lower clouds and can extend the cream section when text grows. No JavaScript is needed.

## Validation

Local browser geometry checked at 320, 360, 390, 748, 750, 768, 1024, 1100, 1280, 1440 and 1920 CSS pixels: no horizontal overflow, copy clears the header, and the CTA stays inside the hero. At the tall 748px portrait layout the CTA is below the viewport and reachable by scrolling. Visual checks covered desktop, tablet and small phones; tablet artwork was lowered to prevent the navigation hiding faces. The 320px menu opens with aligned character cards, Escape returns to the closed menu, and the hero CTA opens the collection containing 10 tees.

Theme Check on a clean copy of the active theme: zero errors and no hero offenses. `git diff --check` passed. Screenshot and geometry evidence is in `C:/Users/krish/.codex/visualizations/2026/10/24/01a16ce0-396f-7010-ad67-f9e94e181d2b/` (`paper-boat-desktop.jpg`, `paper-boat-mobile.jpg`, `paper-boat-responsive-checks.json`). No live upload was performed.

## Desktop prompt

```text
Use case: illustration-story / ads-marketing.
Create an extraordinary original 16:9 widescreen cinematic hero illustration for Jevika & Joy's World. Creative concept: "A little imagination. An enormous adventure." A moment of pure childhood wonder: five best friends have folded a giant SUNSHINE-YELLOW PAPER BOAT, and their imaginary boat has just lifted into the sky, surfing a curling wave of luminous fluffy clouds. The emotion is infectious shared joy, belonging, mischief and the freedom of being little. It should feel like the one unforgettable frame of a beautifully art-directed animated film. This is a rich complete scene, not a character lineup, a product ad or a collage.
Use the FIVE attached turnaround sheets as STRICT CHARACTER IDENTITY references, in order:
1. Jevika: Indian girl, warm skin, expressive brown eyes, voluminous dark curly twin ponytails tied with red stars, white robot-emblem tee, red tartan skirt, white socks and red sneakers.
2. Joy: Indian boy, spiky dark hair, expressive brown eyes, yellow blue-lightning-emblem tee, olive cargo trousers, black/blue/yellow sneakers.
3. Brutus: a believable brindle BOXER dog with black muzzle, floppy ears, white chest and paws, brown collar, recognizable square boxer face; not a puppy of another breed.
4. Minku: little brown monkey with blue eyes, banana-pattern blue bandana, orange M/lightning tee, denim shorts, bare monkey feet, long curled tail.
5. Pinki: orange squirrel girl, green-rimmed glasses, small pink-and-blue hair ornaments, denim pinafore, striped socks, pink shoes and big fluffy tail.
Preserve their faces, hair, fur, proportions and canonical outfits closely. Exactly these five friends appear once each; no additional characters.
STORY AND POSES: Giant handmade folded yellow paper boat occupies the RIGHT 60% of the frame, angled dynamically in threequarter view, pointing toward the lower-left, with crisp origami folds, subtle paper fibres, tactile imperfect hand-folded edges. No wooden ship, no mast, no realistic nautical rigging. Joy is perched securely at the front, laughing in wonder with one hand lifted into the breeze. Jevika beside him leans forward to catch a small glowing star-shaped mote, curls floating lightly in the wind. Brutus has his FRONT paws on the near folded edge, happy face toward the viewer, ears blown back. Minku sits playfully on the higher rear fold, holding on with one hand and waving the other, tail curling in an expressive arc. Pinki stands securely inside the boat behind Jevika, holding a simple rolled-paper telescope, laughing rather than obscuring her face with it. Natural collaborative interaction and a clear emotional connection between friends. Faces large, appealing and unobscured, all clearly readable. Correct limbs, hands and paws, physically plausible contact with boat. The boat and characters together form one strong beautifully balanced silhouette.
WORLD: A spectacular soft cloud ocean with a few distant small floating meadow islands and tiny waterfalls fading into atmospheric distance; one cluster far right, sparse background. A rainbow-like subtle arc made only of warm sunlight, bright sky blue atmosphere, warm cream clouds, a little candy-pink and lavender in cloud shadows. Below the yellow boat, a sweeping splash of cloud curls like sea foam and trails behind it, suggesting flight and momentum without danger. Tiny golden star motes and a few folded paper birds follow the boat, but keep these restrained. NO castle, jungle portal, treasure map or shop. Avoid generic overdecorated fantasy wallpaper.
WEBSITE COMPOSITION IS ESSENTIAL: Left 35-38% of frame is genuinely quiet luminous warm ivory/cream sky and softly graduating clouds, gentle low contrast, safe for a large dark headline and a shopping button later in HTML. All faces, bodies, boat and detailed islands stay RIGHT of x=40%. No dark foliage, flying objects, stars or busy clouds in that copy zone. Top 12% is airy sky for navigation, all heads below that zone. Boat and character extremities fit inside frame with generous edge breathing room; don't crop head, tail or bow. Powerful slightly low camera angle, immersive depth, right-side narrative focus. Do not bake any headline, logo, letters, slogan, button, UI or watermark into artwork. Only small original costume emblems from references remain.
STYLE: World-class polished stylized 3D character animation with lovingly detailed fur, expressive faces and tactile material rendering. Sophisticated cinematic lighting: peach-gold sunlight from upper left, soft cool sky fill, beautifully luminous rim lighting, realistic gentle shadows, rich but controlled saturated palette. Crisp characters and boat, dreamy background depth. Not plastic toy-like, not flat vector, not photoreal humans, not a busy movie poster. Wonder, warmth, motion and personality.
ABSOLUTELY NO displayed products, merchandise, hanging shirts, clothing racks, folded clothing, retail displays, packaging, shopping bags, price tags or advertisements. Their normal character outfits are the only clothing. This image sells the imaginative world and emotional feeling. Generate only the finished wide illustration.
```

## Mobile prompt

```text
Create a 9:16 PORTRAIT mobile website hero companion to reference image 1. Preserve its cinematic 3D animation quality, all FIVE original characters, giant sunshine-yellow origami paper boat, magical cloud ocean, warm sunlit colour palette and emotional story. The other reference images are canonical character identities; Brutus the brindle boxer is accurately shown in image 1.
RECOMPOSE rather than crop. All five characters must be visible with clear expressive faces and correct original clothing, on one giant hand-folded yellow paper boat joyfully riding a cloud wave. Jevika with dark curly star-tied ponytails white robot tee red plaid skirt reaches for one glowing star; Joy spikyhair yellow lightning tee olive cargo trousers laughs and waves; Minku monkey blue banana bandana orange M shirt denim shorts sits on rear fold; Pinki orange squirrel green glasses denim pinafore pink shoes holds rolled-paper telescope aside, her face visible; happy brindle boxer Brutus white chest/paws brown collar leans front paws over near fold, looking at viewer.
LAYOUT: airy sky in top 12% for website navigation. Put all five faces between y=16% and y=40%, arranged naturally in two staggered rows. The whole boat and characters occupy the central upper area y=14% to y=59%, nearly full canvas width with clear margins. Boat's pointed bow fully visible. Keep characters large enough to read on a phone but do not cut anyone off. A beautiful cloud wave curls beneath the boat. LOWER 38% of the canvas, from y=62% onward, must transition smoothly to calm warm ivory/cream clouds (#FFF7E8) with very little texture and no subjects, birds, stars, rainbows or islands. That is empty space for HTML text and button. No hard split or panel. Image bottom is entirely soft cream so it can flow into a cream webpage.
A couple of distant floating meadow islands and a few golden origami birds restricted to the scene edges above y=57%. Rich paper texture, soft expressive faces, detailed hair/fur, joyful interaction, luminous peach-gold sun with cool blue sky fill, beautiful depth. High-end family animation key art, sophisticated and warm, not plastic toys.
Do not include any products, displayed shirts, shop, packaging, shopping bags, signs, headline, lettering, UI or watermarks. Their original character costumes and small emblems are unchanged. Exactly five characters, no duplicate faces or limbs. Generate only the finished seamless portrait illustration.
```

