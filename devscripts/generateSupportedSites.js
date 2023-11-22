const url = `https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/supportedsites.md`;

const matches = {
    broken: /\(\*\*Currently broken\*\*\)(?!\.\S)/,
    parent: /(\[.*\])\(## "netrc machine"\)/,
}

const tags = {
    broken: (str) => str.match(matches.broken) ? {
        matched: str.match(matches.broken)[0],
        value: true,
    } : false,
    parent: (str) => str.match(matches.parent) ? {
        matched: str.match(matches.parent)[0],
        value: str.match(matches.parent)[1].slice(2, -2),
    } : null,
};

const generateDetails = (str) => {
    const thisStringTags = {};

    Object.keys(tags).forEach(tag => {
        const matched = tags[tag](str);

        if(matched) {
            thisStringTags[tag] = matched.value;
            str = str.replace(matched.matched, ``).trim();
        } else {
            thisStringTags[tag] = matched;
        }
    });

    return { ...thisStringTags, description: str || null }
};

const defaultParent = (name) => ({
    name: name || null,
    description: null,
    includes: [],
});

fetch(url).then(res => res.text()).then(res => {
    const obj = {};

    const list = res.split(`\n - `).slice(1);

    list.forEach(item => {
        const matched = item.match(/\*\*.*?\*\*(?!\.\S)/)[0];

        let name = matched.slice(2, -2);
        let tags = generateDetails(item.split(matched).slice(1).join(matched).slice(1).trim());

        if(name.includes(`:`) && !tags.parent) {
            tags.parent = name.split(`:`)[0].trim();
            name = name.split(`:`).slice(1).join(`:`).trim();
        }

        if(tags.parent && name.toLowerCase() !== tags.parent.toLowerCase()) {
            if(!obj[tags.parent.toLowerCase()]) obj[tags.parent.toLowerCase()] = defaultParent(tags.parent);

            obj[tags.parent.toLowerCase()].includes.push({ name, ...tags });
        } else {
            if(!obj[name.toLowerCase()]) obj[name.toLowerCase()] = defaultParent(name);
            
            obj[name.toLowerCase()] = { ...obj[name.toLowerCase()], name, ...tags };
        }
    });

    console.log(JSON.stringify(obj));
});