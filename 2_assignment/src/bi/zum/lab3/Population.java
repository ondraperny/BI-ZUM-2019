package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.api.ga.AbstractPopulation;
import cz.cvut.fit.zum.data.StateSpace;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Population extends AbstractPopulation {

    public Population(AbstractEvolution evolution, int size) {
        individuals = new Individual[size];
        for (int i = 0; i < individuals.length; i++) {
            individuals[i] = new Individual(evolution, true);
            individuals[i].computeFitness();
        }
    }

    /**
     * Method to select individuals from population
     *
     * @param count The number of individuals to be selected
     * @return List of selected individuals
     */
    public List<AbstractIndividual> selectIndividuals(int count) {

//                ArrayList<AbstractIndividual> selected = new ArrayList<AbstractIndividual>();
//  //       example of random selection of N individuals
//        Random r = new Random();
//        AbstractIndividual individual = individuals[r.nextInt(individuals.length)];
//        while (selected.size() < count) {
//            selected.add(individual);
//            individual = individuals[r.nextInt(individuals.length)];
//        }

        // tournament
        // there will be 'count' tournaments, each with 'tournamentSize' competitors
        int tournamentSize = 5;
        ArrayList<AbstractIndividual> selected = new ArrayList<AbstractIndividual>();
        Random r = new Random();
        AbstractIndividual best, next;

        while (selected.size() < count) {
            best = individuals[r.nextInt(individuals.length)];

            for (int i = 2; i < tournamentSize; ++i) {
                next = individuals[r.nextInt(individuals.length)];
                if(next.getFitness() > best.getFitness()) {
                    best = next;
                }
            }
            selected.add(best);
        }

        return selected;
    }
}
