<script src="https://static01.nyt.com/newsgraphics/2013/01/07/movie-network/72ae3b8d92ecc7a67c00babd2a75f34bfdacb3a7/d3.v3.min.js"></script>
                                <script>
                                    (function() {

                                        var width = 970,
                                            height = 1500,
                                            mugDiameter = 40,
                                            mugSize = 80;

                                        var bounds = d3.geom.polygon([
                                            [0, 0],
                                            [0, height],
                                            [width, height],
                                            [width, 0]
                                        ]);

                                        var awardType = {
                                            "Best Actor": "actor",
                                            "Best Actress": "actor",
                                            "Best Supporting Actor": "actor",
                                            "Best Supporting Actress": "actor",
                                            "Best Picture": "producer",
                                            "Best Director": "director"
                                        };

                                        var awardRank = {
                                            "Best Picture": 1,
                                            "Best Director": 2,
                                            "Best Actor": 3,
                                            "Best Actress": 3,
                                            "Best Supporting Actor": 4,
                                            "Best Supporting Actress": 4
                                        };

                                        var color = self.color = d3.scale.ordinal()
                                            .domain(["actor", "producer", "director"])
                                            .range(["#3182bd", "#42a48d", "#7d4098", "#969696", "#969696", "#969696", "#969696", "#969696"]);

                                        var svg = d3.select(".g-graphic").insert("svg", ".g-note")
                                            .attr("width", width)
                                            .attr("height", height);

                                        svg.append("defs").append("clipPath")
                                            .attr("id", "g-mug-clip")
                                            .append("circle")
                                            .attr("r", mugDiameter / 2);

                                        var tooltip = d3.select(".g-graphic").append("div")
                                            .attr("class", "g-tooltip")
                                            .style("display", "none");

                                        var tooltipPath = tooltip.append("svg")
                                            .attr("class", "g-tooltip-path");

                                        tooltipPath.append("path");

                                        var tooltipContent = tooltip.append("div")
                                            .style("position", "relative")
                                            .style("z-index", 2)
                                            .style("padding", "8px");

                                        var tooltipName = tooltipContent.append("div")
                                            .attr("class", "g-name");

                                        var tooltipDescription = tooltipContent.append("div")
                                            .attr("class", "g-description");

                                        var overlay = d3.select(".g-graphic").append("svg")
                                            .attr("width", width)
                                            .attr("height", height)
                                            .style("z-index", 3);

                                        d3.json("https://static01.nyt.com/newsgraphics/2013/01/07/movie-network/72ae3b8d92ecc7a67c00babd2a75f34bfdacb3a7/network.json", function(error, network) {

                                            network.persons.forEach(function(a, i) {
                                                a.index = i;
                                                a.links = [];
                                            });

                                            network.movies.forEach(function(m, i) {
                                                m.index = i;
                                                m.nominations = [];
                                                m.links.forEach(function(l) {
                                                    var p = l.person = network.persons[l.person];
                                                    l.movie = m;
                                                    p.links.push(l);
                                                    return p;
                                                });
                                            });

                                            network.persons.forEach(function(a, i) {
                                                a.nominations.forEach(function(n) {
                                                    n.movie = network.movies[n.movie];
                                                    n.movie.nominations.push(n);
                                                    n.person = a;
                                                });
                                            });

                                            svg.append("g")
                                                .attr("class", "g-movie-clips")
                                                .selectAll("clipPath")
                                                .data(network.movies)
                                                .enter().append("clipPath")
                                                .attr("id", function(d, i) {
                                                    return "g-movie-clip-" + i;
                                                })
                                                .append("circle")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.x + "," + d.y + ")";
                                                })
                                                .attr("r", 80);

                                            svg.append("g")
                                                .attr("class", "g-person-hulls")
                                                .selectAll("path")
                                                .data(d3.merge(network.persons.map(function(p) {
                                                    return p.links;
                                                })))
                                                .enter().append("path")
                                                .sort(function(a, b) {
                                                    return d3.descending(a.role, b.role);
                                                })
                                                .style("stroke", function(d) {
                                                    return d3.interpolate(color(d.role), "#fff")(.75);
                                                })
                                                .attr("d", movieToPersonLink);

                                            svg.append("g")
                                                .attr("class", "g-movie-links")
                                                .selectAll("path")
                                                .data(d3.merge(network.movies.map(function(m) {
                                                    return m.links;
                                                })))
                                                .enter().append("path")
                                                .classed("g-current-nomination", currentNomination)
                                                .classed("g-win", win)
                                                .attr("d", movieToPersonLink);

                                            svg.append("g")
                                                .attr("class", "g-movie-dots")
                                                .selectAll("circle")
                                                .data(network.movies)
                                                .enter().append("circle")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.x + "," + d.y + ")";
                                                })
                                                .classed("g-current-nomination", function(m) {
                                                    return m.links.some(currentNomination);
                                                })
                                                .classed("g-win", function(m) {
                                                    return m.links.some(win);
                                                })
                                                .attr("r", function(m) {
                                                    return m.links.some(currentNomination) ? 5 : 3;
                                                });

                                            svg.append("g")
                                                .attr("class", "g-movie-labels")
                                                .selectAll("text")
                                                .data(network.movies.filter(function(m) {
                                                    return m.links.some(currentNomination) ||
                                                        m.links.some(win);
                                                }))
                                                .enter().append("text")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.label.x + "," + d.label.y + ")";
                                                })
                                                .classed("g-current-best-picture-nomination", function(m) {
                                                    return m.links.some(currentBestPictureNomination);
                                                })
                                                .classed("g-current-nomination", function(m) {
                                                    return m.links.some(currentNomination);
                                                })
                                                .classed("g-win", function(m) {
                                                    return m.links.some(win);
                                                })
                                                .attr("dy", ".35em")
                                                .text(function(m) {
                                                    return m.name;
                                                });

                                            var movieTarget = overlay.append("g")
                                                .attr("class", "g-voronoi")
                                                .selectAll("path")
                                                .data(d3.geom.voronoi(network.movies.map(function(d) {
                                                    return [d.x, d.y];
                                                })).map(function(d) {
                                                    return bounds.clip(d);
                                                }))
                                                .enter().append("path")
                                                .attr("clip-path", function(d, i) {
                                                    return "url(#g-movie-clip-" + i + ")";
                                                })
                                                .attr("d", function(d) {
                                                    return "M" + d.join("L") + "Z";
                                                })
                                                .datum(function(d, i) {
                                                    return network.movies[i];
                                                })
                                                .on("mouseover", mouseoverMovie)
                                                .on("mouseout", mouseout)
                                                .on("click", click);

                                            var personTarget = overlay.selectAll(".g-person-target")
                                                .data(network.persons)
                                                .enter().append("circle")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.x + "," + d.y + ")";
                                                })
                                                .attr("class", "g-person-target")
                                                .attr("r", mugDiameter / 2 + 2.5)
                                                .style("stroke-width", 5)
                                                .on("mouseover", mouseoverPerson)
                                                .on("mouseout", mouseout);

                                            var personDot = svg.append("g")
                                                .attr("class", "g-person-dots")
                                                .selectAll("g")
                                                .data(network.persons)
                                                .enter().append("g")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.x + "," + d.y + ")";
                                                });

                                            personDot.append("circle")
                                                .attr("r", mugDiameter / 2 + 2.5)
                                                .style("stroke", function(d) {
                                                    return d3.lab(color(d.type)).darker(.2);
                                                })
                                                .style("stroke-width", 5);

                                            personDot.append("image")
                                                .attr("xlink:href", "https://static01.nyt.com/newsgraphics/2013/01/07/movie-network/72ae3b8d92ecc7a67c00babd2a75f34bfdacb3a7/mugs.jpg")
                                                .attr("x", function(d, i) {
                                                    return -mugDiameter / 2 - mugDiameter * (i % 9);
                                                })
                                                .attr("y", function(d, i) {
                                                    return -mugDiameter / 2 - mugDiameter * (i / 9 | 0);
                                                })
                                                .attr("width", 9 * mugDiameter)
                                                .attr("height", 6 * mugDiameter)
                                                .attr("clip-path", "url(#g-mug-clip)")
                                                .style("pointer-events", "none");

                                            var personLabel = svg.append("g")
                                                .attr("class", "g-person-labels")
                                                .selectAll("g")
                                                .data(network.persons)
                                                .enter().append("g")
                                                .attr("transform", function(d) {
                                                    return "translate(" + d.label.x + "," + d.label.y + ")";
                                                })
                                                .style("pointer-events", "none");

                                            personLabel.append("text")
                                                .attr("class", "g-halo")
                                                .attr("dy", ".35em")
                                                .text(function(d) {
                                                    return d.name;
                                                });

                                            personLabel.append("text")
                                                .attr("dy", ".35em")
                                                .style("fill", function(d) {
                                                    return d3.lab(color(d.type)).darker(.2);
                                                })
                                                .text(function(d) {
                                                    return d.name;
                                                });

                                            var gkey = svg.append("g")
                                                .attr("class", "g-key")
                                                .attr("transform", "translate(" + (width - 180) + ",16)");

                                            gkey.append("text")
                                                .style("font-weight", "bold")
                                                .attr("y", -6)
                                                .text("Current nominations");

                                            var key = gkey.selectAll("g")
                                                .data(color.domain().slice(0, 3).concat(["Multiple roles"]))
                                                .enter().append("g")
                                                .attr("transform", function(d, i) {
                                                    return "translate(0," + i * 20 + ")";
                                                });

                                            key.append("circle")
                                                .attr("r", 6)
                                                .attr("cx", 9)
                                                .attr("cy", 9)
                                                // .style("fill-opacity", .5)
                                                .style("opacity", .6)
                                                .style("fill", "none")
                                                .style("stroke", function(d) {
                                                    return d3.lab(color(d)).darker(.2);
                                                })
                                                .style("stroke-width", 5);

                                            key.append("text")
                                                .attr("x", 23)
                                                .attr("y", 9)
                                                .attr("dy", ".35em")
                                                .text(function(d) {
                                                    var first = d.substring(0, 1),
                                                        rest = d.substring(1);
                                                    return first.toUpperCase() + rest.replace(/-/g, " and ");
                                                });

                                            function mouseoverPerson(p) {
                                                var g = svg.insert("g", ".g-movie-dots")
                                                    .attr("class", "g-movie-links g-active");

                                                g.selectAll("path")
                                                    .data(p.links)
                                                    .enter().append("path")
                                                    .attr("d", personToMovieLink)
                                                    .style("stroke-dasharray", "0,250")
                                                    .transition()
                                                    .ease("cubic-in")
                                                    .style("stroke-dasharray", "250,250");

                                                d3.selectAll(".g-person-dots circle")
                                                    .filter(function(o) {
                                                        return o === p;
                                                    })
                                                    .classed("g-active", true);
                                            }

                                            function mouseoverMovie(m) {
                                                var g = svg.insert("g", ".g-movie-dots")
                                                    .attr("class", "g-movie-links g-active");

                                                g.selectAll("path")
                                                    .data(m.links)
                                                    .enter().append("path")
                                                    .attr("d", movieToPersonLink)
                                                    .style("stroke-dasharray", "0,250")
                                                    .transition()
                                                    .ease("cubic-in")
                                                    .style("stroke-dasharray", "250,250");

                                                d3.selectAll(".g-movie-dots circle")
                                                    .filter(function(o) {
                                                        return o === m;
                                                    })
                                                    .classed("g-active", true);

                                                d3.selectAll(".g-person-dots circle")
                                                    .filter(function(p) {
                                                        return p.links.some(function(l) {
                                                            return l.movie === m;
                                                        });
                                                    })
                                                    .classed("g-active", true);

                                                tooltip
                                                    .style("display", null);

                                                tooltipName
                                                    .text(m.name + " (" + m.year + ")");

                                                tooltipDescription
                                                    .html(m.nominations.length ?
                                                        "\n" + d3.nest()
                                                        .key(function(n) {
                                                            return n.name;
                                                        })
                                                        .sortKeys(function(a, b) {
                                                            return d3.ascending(awardRank[a] || 100, awardRank[b] || 100) ||
                                                                d3.ascending(a, b);
                                                        })
                                                        .entries(m.nominations)
                                                        .map(function(n) {
                                                            return n.key +
                                                                " - <span class=g-" + awardType[n.key] + ">" + n.values.map(function(n) {
                                                                    return n.person.name;
                                                                }).join(", ") + "</span>" +
                                                                (n.values.some(function(n) {
                                                                    return n.won;
                                                                }) ? "\xa0\u2713" : "");
                                                        }).join("<br>") :
                                                        "");

                                                var tooltipRect = tooltipContent.node().getBoundingClientRect(),
                                                    tooltipOrient = d3.mean(m.links, function(d) {
                                                        return d.person.y;
                                                    }) < m.y ? "bottom" : "top";

                                                switch (tooltipOrient) {
                                                    case "top":
                                                        {
                                                            tooltipPath
                                                            .attr("width", tooltipRect.width + 4)
                                                            .attr("height", tooltipRect.height + 10)
                                                            .style("margin-left", "-2px")
                                                            .style("margin-top", null)
                                                            .select("path")
                                                            .attr("transform", "translate(2,0)")
                                                            .attr("d", "M0,6" +
                                                                "a6,6 0 0,1 6,-6" +
                                                                "H" + (tooltipRect.width - 6) +
                                                                "a6,6 0 0,1 6,6" +
                                                                "v" + (tooltipRect.height - 12) +
                                                                "a6,6 0 0,1 -6,6" +
                                                                "H" + (tooltipRect.width / 2 + 6) +
                                                                "l-6,6" +
                                                                "l-6,-6" +
                                                                "H6" +
                                                                "a6,6 0 0,1 -6,-6" +
                                                                "z");

                                                            tooltip
                                                            .style("left", (m.x - tooltipRect.width / 2) + "px")
                                                            .style("top", (m.y - tooltipRect.height - 10) + "px");
                                                            break;
                                                        }
                                                    case "bottom":
                                                        {
                                                            tooltipPath
                                                            .attr("width", tooltipRect.width + 4)
                                                            .attr("height", tooltipRect.height + 10)
                                                            .style("margin-left", "-2px")
                                                            .style("margin-top", "-10px")
                                                            .select("path")
                                                            .attr("transform", "translate(2,10)")
                                                            .attr("d", "M0,6" +
                                                                "a6,6 0 0,1 6,-6" +
                                                                "H" + (tooltipRect.width / 2 - 6) +
                                                                "l6,-6" +
                                                                "l6,6" +
                                                                "H" + (tooltipRect.width - 6) +
                                                                "a6,6 0 0,1 6,6" +
                                                                "v" + (tooltipRect.height - 12) +
                                                                "a6,6 0 0,1 -6,6" +
                                                                "H6" +
                                                                "a6,6 0 0,1 -6,-6" +
                                                                "z");

                                                            tooltip
                                                            .style("left", (m.x - tooltipRect.width / 2) + "px")
                                                            .style("top", (m.y + 10) + "px");
                                                            break;
                                                        }
                                                }
                                            }

                                            function click() {
                                                tooltip.style("display", "none");
                                            }

                                            function mouseout() {
                                                d3.selectAll(".g-movie-links.g-active")
                                                    .remove();

                                                d3.selectAll(".g-active")
                                                    .classed("g-active", false)
                                                    .style("stroke-dasharray", null);

                                                tooltip.style("display", "none");
                                            }

                                            function movieToPersonLink(d) {
                                                return "M" + d.movie.x + "," + d.movie.y +
                                                    "S" + d.x + "," + d.y +
                                                    " " + d.person.x + "," + d.person.y;
                                            }

                                            function personToMovieLink(d) {
                                                return "M" + d.person.x + "," + d.person.y +
                                                    "C" + d.x + "," + d.y +
                                                    " " + d.movie.x + "," + d.movie.y +
                                                    " " + d.movie.x + "," + d.movie.y;
                                            }

                                            // function hull(p) {
                                            //   return p.links.map(movieToPersonLink).join("");
                                            // }

                                            function currentNomination(l) {
                                                return l.person.nominations.some(function(n) {
                                                    return n.year === 2013 && n.movie === l.movie;
                                                });
                                            }

                                            function currentBestPictureNomination(l) {
                                                return l.person.nominations.some(function(n) {
                                                    return n.year === 2013 && n.movie === l.movie && n.name === "Best Picture";
                                                });
                                            }

                                            function win(l) {
                                                return l.person.nominations.some(function(n) {
                                                    return n.won && n.movie === l.movie;
                                                });
                                            }
                                        });

                                    })()
                                </script>
                            </div>
                            <div class="insetHFullWidth">
                                <div id="interactiveFooter" class="opposingFloatControl wrap">
                                    <div class="metaData element1">
                                        <div class="module">
                                            <span class="byline">By MIKE BOSTOCK, SHAN CARTER and JOSH KELLER</span>
                                        </div>
                                        <div class="module">
                                            <p class="credit">Source: IMDb</p>
                                        </div>
                                    </div>
                                    <div class="element2">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <footer class="pageFooter">
                <div class="inset">
                    <nav class="pageFooterNav">
                        <ul class="pageFooterNavList wrap">
                            <li class="firstItem"><a href="https://www.nytimes.com/content/help/rights/copyright/copyright-notice.html">&#xA9; 2016 The New York Times Company</a></li>
                            <li><a href="http://spiderbites.nytimes.com/">Site Map</a></li>
                            <li><a href="https://www.nytimes.com/privacy">Privacy</a></li>
                            <li><a href="https://www.nytimes.com/ref/membercenter/help/privacy.html#pp">Your Ad Choices</a></li>
                            <li><a href="http://www.nytimes.whsites.net/mediakit/">Advertise</a></li>
                            <li><a href="https://www.nytimes.com/content/help/rights/sale/terms-of-sale.html ">Terms of Sale</a></li>
                            <li><a href="https://www.nytimes.com/ref/membercenter/help/agree.html">Terms of Service</a></li>
                            <li><a href="http://www.nytco.com/careers">Work With Us</a></li>
                            <li><a href="https://www.nytimes.com/rss">RSS</a></li>
                            <li><a href="https://www.nytimes.com/membercenter/sitehelp.html">Help</a></li>
                            <li><a href="https://www.nytimes.com/ref/membercenter/help/infoservdirectory.html">Contact Us</a></li>
                            <li class="lastItem"><a href="https://myaccount.nytimes.com/membercenter/feedback.html">Site Feedback</a></li>
                        </ul>
                    </nav>
                </div>
            </footer>
        </div>
    </div>
    <script language="JavaScript" type="text/javascript">
        NYTD.require('https://static01.nyt.com/js/app/homepage/articleCommentCounts.js');
    </script>
    <script type="text/javascript" language="JavaScript">
        ArticleCommentCounts.apply()
    </script>
</body>

</html>