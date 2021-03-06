# -*- coding: utf-8 -*-

#    Copyright 2016 Mirantis, Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from packetary.objects import PackagesForest
from packetary.tests import base
from packetary.tests.stubs import generator


class TestPackagesForest(base.TestCase):
    def setUp(self):
        super(TestPackagesForest, self).setUp()

    def _add_packages(self, tree, packages):
        for pkg in packages:
            tree.add(pkg)

    def _generate_packages(self, forest):
        packages1 = [
            generator.gen_package(
                name="package1", version=1, mandatory=True,
                requires=None
            ),
            generator.gen_package(
                name="package2", version=1,
                requires=None
            ),
            generator.gen_package(
                name="package3", version=1,
                requires=[generator.gen_relation("package5")]
            )
        ]
        packages2 = [
            generator.gen_package(
                name="package4", version=1, mandatory=True,
                requires=None
            ),
            generator.gen_package(
                name="package5", version=1,
                requires=[generator.gen_relation("package2")]
            ),
        ]
        self._add_packages(forest.add_tree(priority=10), packages1)
        self._add_packages(forest.add_tree(priority=10), packages2)

    def test_add_tree(self):
        forest = PackagesForest()
        tree = forest.add_tree(priority=10)
        self.assertIs(tree, forest.trees[10])
        # test that trees with the same priority are merged
        tree = forest.add_tree(priority=10)
        self.assertEqual(1, len(forest.trees))
        tree = forest.add_tree(priority=50)
        self.assertEqual(2, len(forest.trees))

    def test_find(self):
        forest = PackagesForest()
        p11 = generator.gen_package(name="package1", version=1)
        p12 = generator.gen_package(name="package1", version=2)
        p21 = generator.gen_package(name="package2", version=1)
        p22 = generator.gen_package(name="package2", version=2)
        p33 = generator.gen_package(name="package2", version=10)
        self._add_packages(forest.add_tree(priority=10), [p11, p22])
        self._add_packages(forest.add_tree(priority=10), [p12, p21])
        self._add_packages(forest.add_tree(priority=20), [p33])
        self.assertEqual(
            p11, forest.find(generator.gen_relation("package1", ["=", 1]))
        )
        self.assertEqual(
            p12, forest.find(generator.gen_relation("package1", [">=", 1]))
        )
        self.assertEqual(
            p12, forest.find(generator.gen_relation("package1", [">", 1]))
        )
        self.assertEqual(p22, forest.find(generator.gen_relation("package2")))
        self.assertEqual(
            p21, forest.find(generator.gen_relation("package2", ["<", 2]))
        )
        # select package from the repo with highest priority
        # p33 has version 10, but in the repo with lower priority
        self.assertEqual(
            p22, forest.find(generator.gen_relation("package2", [">=", 2]))
        )

    def test_get_packages(self):
        forest = PackagesForest()
        self._generate_packages(forest)
        packages = forest.get_packages(
            [generator.gen_relation("package3")]
        )
        self.assertItemsEqual(
            ["package2", "package3", "package5"],
            (x.name for x in packages)
        )
