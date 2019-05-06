# ponder-and-circle-ci-test

## Introduction

This is a small Cplex based solver to solve the April 2019 Solver challenge:

https://www.research.ibm.com/haifa/ponderthis/challenges/April2019.html

The task is as follows:

Find nine different prime numbers that can be placed in a 3x3 square in such a way that the average of every row, column, and diagonal is also a prime number.

## How the problem is solved

1. The problem contains a simple method _primes(lower, upper)_ to generate an ordered list of prime numbers between _lower_ and _upper_. Not the fastest approach. We basically iterate through all numbers in our interval and then test this number for every divisior between 2 and the chosen number. If there is a remainder, the loop is stopped. If the loop reaches its end, the number is a prime number and is added to the list. Not the most efficient approach, but good enough, since this is not the bottleneck for once. If we are interested in speeding this up, we can divide by the prime numbers we have already found already and skip all divisors that are greater than the square root of the number, instead of dividing through all numbers (assuming a <= 2).
2. The magic is in the method _main()_ - we are using a binary linear problem to solve this problem. The variables are defined as follows: _variable[(i, j, pnum)]_ == 1 if the number in the square in row _i_ and column _j_ is equal to the prime number pnum. It is 0 otherwise.
3. We now have several constraints that need to be satisfied and can be easily implemented as linear constraints: a) every cell in the square needs to contain exactly 1 number, b) every prime number can be contained in the square at most once, c) Looking at each diagonal, row and column in the square, we need to forbid combinations of prime numbers that lead to average that is not a prime number.

## Comments

1. Cplex finds a solution to this problem quickly, however the method does not scale well at all. With a 4x4 square, the number of linear constraints that is added gets very high.
2. A simple backtracking solution similar to a Sudoku solver would work very well on this type of problem.

## Circle-Ci integration

I have used this small project to test how to use CircleCi to automatically excecute unit tests and, once that is done, call a URL on a server (which, on the server, might trigger a pull request to get the latest version of the code from GitHub).

If the circle ci configuration (.circleci/config.yml) is added to a repository that is structured like this, all that is left to do, is to sign up to circle-ci (use GitHub to authentificate), select the correct repository and then hit "start build". Every time a commit is pushed to any branch in the project, circle-ci runs all the tests that are specified in the test command. 

Note, that I have only include "prime_number_test" but not the "solver_test". The reason for this is, that this requires an unlimited license of Cplex, which is not available in a standard docker image. It is not a problem to create a docker image that includes a Cplex installation (https://support.circleci.com/hc/en-us/articles/360000217868-How-do-I-create-a-custom-docker-image-for-CircleCI- ), however, since the image needs to be hosted on Dockerhub or a comparable service, make sure that your Cplex license actually allows you to install Cplex inside a docker container that is not hosted on your own hardware.

The last part of the docker configuration file contains a command "curl http://.......:5000/notify-change/)". The idea with this is, that whenever we push something to GitHub, we might want, that this code is pulled from GitHub onto some server to deploy the latest version of the code. There is a standard way of doing this for AWS clouds and other cloud based service providers, but also for privately hosted servers (https://circleci.com/docs/2.0/deployment-integrations/#ssh). I chose to use this other way, because the scenario in our (real) case is, that the code needs to be deployed to serveral servers. Only one of them is exposed to the internet, while the others can only be accessed through a VPN connection. The servers can be accessed from each other though. On these servers, a small Flask application is running. This application is used to trigger the update and notify all "dependent" servers to update aswell.
