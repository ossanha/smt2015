# What is it ?

This repository contains data and detailed reports dealing with the first real-sized tests for `SMTpp`, 
with instructions as to how to reproduce and check our results.

This repository is divided into the following subdirectories:
: parser
    This directory contains the time comparisons and
    * Z3 4.3.2
    * Alt-Ergo 0.99.1 (-parse-only)
    * smtlib2
    * jSMTLIB
    * smtpp.byt
    * smtpp.opt 
    * smtpp.opt -detect-logic

: logic-detection
    Contains the reports generated from runs of `smtpp.opt -detect-logic` on
    the whole SMT-LIB.

: undef-unused
    Contains the reports generated from runs `smtpp.opt -undef-unused` on the whole 
    SMT-LIB

# How to reproduce ?

Steps to reproduce are detailed in each specific repository. 

Open an issue on this github repository in case of problems. We’ll be glad to help.
