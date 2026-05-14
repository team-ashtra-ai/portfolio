# Asset QA

| Check | Result |
| --- | --- |
| Local paths | All generated asset paths are relative and local to the site folder. |
| No licensed images | No external stock/photo/map/dashboard/font/image sources are used. |
| No fake proof | No fake client logos, certification badges, partner logos, testimonials, staff portraits, or media logos are generated. |
| Responsive crops | Hero desktop/tablet/mobile SVG crops are generated per page; CSS preserves object-fit and dimensions. |
| Accessibility | Informative images receive purpose alt text; repeated decorative icons/thumbs use empty alt. |
| Performance | SVG is used for scalable visuals; PNG is limited to favicons/touch/social icons; lazy loading is used off hero. |
| Theme fit | Assets follow Logistics platform with blue enterprise polish, orange action, and shipment dashboards and Ports, shipment dashboards, containers, trade lanes. |

## Asset Handoff Documentation

The public site no longer exposes an asset-system HTML route. Asset inventories remain in the docs folder and local asset tree for QA and handoff; public navigation uses only the 10 core pages and 7 universal utility pages.
