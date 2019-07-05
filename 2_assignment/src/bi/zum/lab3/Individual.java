package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.data.Edge;
import cz.cvut.fit.zum.data.StateSpace;
import cz.cvut.fit.zum.util.Pair;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

public class Individual extends AbstractIndividual {

    private double fitness = Double.NaN;
    private AbstractEvolution evolution;
    boolean genotype[];

    Random random;

    /**
     * Creates a new individual
     *
     * @param evolution The evolution object
     * @param randomInit <code>true</code> if the individial should be
     * initialized randomly (we do wish to initialize if we copy the individual)
     */
    public Individual(AbstractEvolution evolution, boolean randomInit) {
        this.evolution = evolution;

        Random r = new Random();
        int numberOfNodes = evolution.getNodesCount();
        this.genotype = new boolean[numberOfNodes];
        if (randomInit) {

            for (int i = 0; i < numberOfNodes; ++i) {
                this.genotype[i] = r.nextBoolean();
            }
            this.repairGenotype();

        }

    }

    @Override
    public boolean isNodeSelected(int j) {
        return this.genotype[j];
    }

    /**
     * Evaluate the value of the fitness function for the individual. After the
     * fitness is computed, the <code>getFitness</code> may be called
     * repeatedly, saving computation time.
     */
    @Override
    public void computeFitness() {
        this.fitness = 0;

        for (int i = 0; i < this.genotype.length; ++i) {
            fitness += (genotype[i]) ? 0 : 1;
        }
    }

    /**
     * Only return the computed fitness value
     *
     * @return value of fitness fucntion
     */
    @Override
    public double getFitness() {
        return this.fitness;
    }

    /**
     * Does random changes in the individual's genotype, taking mutation
     * probability into account.
     *
     * @param mutationRate Probability of a bit being inverted, i.e. a node
     * being added to/removed from the vertex cover.
     */
    @Override
    public void mutate(double mutationRate) {
        for (int i = 0; i < this.genotype.length; ++i) {
            if (mutationRate > ThreadLocalRandom.current().nextDouble(0.0, 1.0)) {
                genotype[i] = !genotype[i];
            }
        }
        this.repairGenotype();
    }

    /**
     * Crosses the current individual over with other individual given as a
     * parameter, yielding a pair of offsprings.
     *
     * @param other The other individual to be crossed over with
     * @return A couple of offspring individuals
     */
    @Override
    public Pair crossover(AbstractIndividual other) {

        Pair<Individual, Individual> result = new Pair();
        Individual oth = (Individual) other;

        result.a = new Individual(this.evolution, false);
        result.b = new Individual(oth.evolution, false);

        int firstCrossover = ThreadLocalRandom.current().nextInt(0, this.genotype.length + 1);
        int secondCrossover = ThreadLocalRandom.current().nextInt(0, this.genotype.length + 1);

        if (secondCrossover > firstCrossover) {
            int temp = firstCrossover;
            firstCrossover = secondCrossover;
            secondCrossover = temp;
        }

        for (int i = 0; i < this.genotype.length; ++i) {
            result.a.genotype[i] = this.genotype[i];
            result.b.genotype[i] = oth.genotype[i];
        }

        boolean temp;
        for (int i = firstCrossover; i < secondCrossover; ++i) {
            result.a.genotype[i] = oth.genotype[i];
            result.b.genotype[i] = this.genotype[i];
        }
        result.a.repairGenotype();
        result.b.repairGenotype();

        return result;
    }

    /**
     * When you are changing an individual (eg. at crossover) you probably don't
     * want to affect the old one (you don't want to destruct it). So you have
     * to implement "deep copy" of this object.
     *
     * @return identical individual
     */
    @Override
    public Individual deepCopy() {
        Individual newOne = new Individual(evolution, false);
        System.arraycopy(this.genotype, 0, newOne.genotype, 0, this.genotype.length);
        newOne.fitness = this.fitness;
        return newOne;
    }

    /**
     * Return a string representation of the individual.
     *
     * @return The string representing this object.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        /* TODO: implement own string representation, such as a comma-separated
         * list of indices of nodes in the vertex cover
         */
        sb.append(super.toString());

        return sb.toString();
    }

    private void repairGenotype() {
        Random random = new Random();
        for (Edge e : StateSpace.getEdges()) {
            if (!this.genotype[e.getFromId()]
                    && !this.genotype[e.getToId()]) {
                if (random.nextBoolean()) {
                    this.genotype[e.getFromId()] = true;
                } else {
                    this.genotype[e.getFromId()] = true;
                }
            }
        }
    }

}
