const CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
};

exports.handler = async (event) => {
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers: CORS_HEADERS, body: '' };
    }

    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, body: 'Method Not Allowed' };
    }

    let formData;
    try {
        formData = JSON.parse(event.body);
    } catch (e) {
        return {
            statusCode: 400,
            headers: CORS_HEADERS,
            body: JSON.stringify({ error: 'Invalid JSON body' })
        };
    }

    const prompt = buildPortfolioPrompt(formData);

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-4o-mini',
                max_tokens: 4000,
                messages: [{ role: 'user', content: prompt }]
            })
        });

        const data = await response.json();

        if (!response.ok) {
            return {
                statusCode: response.status,
                headers: CORS_HEADERS,
                body: JSON.stringify({ error: data.error?.message || 'OpenAI API error' })
            };
        }

        return {
            statusCode: 200,
            headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
            body: JSON.stringify({ html: data.choices[0].message.content })
        };

    } catch (error) {
        return {
            statusCode: 500,
            headers: CORS_HEADERS,
            body: JSON.stringify({ error: error.message })
        };
    }
};

function buildPortfolioPrompt(data) {
    const {
        name = '',
        email = '',
        phone = '',
        major = '',
        specialization = '',
        linkedin = '',
        desiredPosition = '',
        jobAd = '',
        colors = {},
        textResources = [],
        htmlResources = [],
        markdownResources = [],
        urlResources = []
    } = data;

    const colorBlock = (colors && Object.keys(colors).length > 0)
        ? `Color scheme:
- Primary:   ${colors.primary   || '(choose professionally)'}
- Secondary: ${colors.secondary || '(choose professionally)'}
- Accent:    ${colors.accent    || '(choose professionally)'}
- Dark:      ${colors.dark      || '(choose professionally)'}
- Light:     ${colors.light     || '(choose professionally)'}`
        : `Color scheme: Choose a modern, professional palette suited for a ${major} graduate.`;

    const resourceBlocks = [];

    if (textResources?.length) {
        resourceBlocks.push('--- Text Resources ---\n' + textResources.map(r =>
            `Section: ${r.section || 'general'}\nContent: ${r.main || ''}\nUsage notes: ${r.description || 'include as-is'}`
        ).join('\n\n'));
    }
    if (htmlResources?.length) {
        resourceBlocks.push('--- HTML Resources ---\n' + htmlResources.map(r =>
            `Content: ${r.main || ''}\nUsage notes: ${r.description || 'use as inspiration'}`
        ).join('\n\n'));
    }
    if (markdownResources?.length) {
        resourceBlocks.push('--- Markdown Resources ---\n' + markdownResources.map(r =>
            `Content: ${r.main || ''}\nUsage notes: ${r.description || 'use as inspiration'}`
        ).join('\n\n'));
    }
    if (urlResources?.length) {
        resourceBlocks.push('--- Reference URLs ---\n' + urlResources.map(r =>
            `URL: ${r.main || ''}\nUsage notes: ${r.description || 'use as inspiration'}`
        ).join('\n\n'));
    }

    return `You are an expert web developer and career coach. Generate a complete, professional, single-file portfolio website for a recent college graduate.

GRADUATE PROFILE:
- Name:            ${name}
- Email:           ${email}
- Phone:           ${phone}
- Major:           ${major}
- Specialization:  ${specialization || 'none specified'}
- LinkedIn:        ${linkedin || 'not provided'}
- Desired Position: ${desiredPosition || 'relevant to their major'}

JOB TARGET:
${jobAd ? jobAd : 'No specific job ad provided — optimize for their major and desired position.'}

${colorBlock}

${resourceBlocks.length > 0 ? 'PORTFOLIO RESOURCES:\n' + resourceBlocks.join('\n\n') : ''}

REQUIREMENTS:
1. Output a complete, single-file HTML document with all CSS and JS inline.
2. Mobile-responsive layout.
3. Include sections most relevant to a ${major} graduate (e.g. About, Skills, Projects/Experience, Education, Contact). Omit sections that don't apply.
4. If a job ad is provided, tailor the language and highlighted skills to match it.
5. Where real content is missing, use realistic placeholder text clearly marked [PLACEHOLDER: description].
6. Modern, clean design — professional enough for a job application.
7. Output ONLY the raw HTML — no explanation, no markdown fences — starting with <!DOCTYPE html>.`;
}
