# Asset QA

| Check | Result |
| --- | --- |
| Local paths | All generated asset paths are relative and local to the site folder. |
| No licensed images | No external stock/photo/map/dashboard/font/image sources are used. |
| No fake proof | No fake client logos, certification badges, partner logos, testimonials, staff portraits, or media logos are generated. |
| Responsive crops | Hero desktop/tablet/mobile SVG crops are generated per page; CSS preserves object-fit and dimensions. |
| Accessibility | Informative images receive purpose alt text; repeated decorative icons/thumbs use empty alt. |
| Performance | SVG is used for scalable visuals; PNG is limited to favicons/touch/social icons; lazy loading is used off hero. |
| Theme fit | Assets follow Minimal product marketing with stark surfaces, centered copy, and energy-product proof and Solar roofs, batteries, energy app panels. |

## Static Asset System Page

`asset-system.html` displays local assets for brand, logo, favicon, images, video posters, icons, illustrations, typography, CSS, JavaScript, animation, SEO, Open Graph, social sharing, header, footer, form, analytics, cookie, accessibility, multilingual, blog, service, industry, case study, downloadable, legal, and trust/proof categories. Files live under this site's own `assets/` tree and are linked from the site navigation.
